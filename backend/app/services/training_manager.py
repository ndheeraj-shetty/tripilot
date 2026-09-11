import asyncio
import os
import sys
import logging
import time
from typing import Dict, Any, Optional, List
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.repositories.project_repo import ProjectRepository
from app.repositories.session_repo import SessionRepository
from app.launcher.process_manager import WindowsProcessManager
from app.monitoring.system_collector import SystemCollector
from app.websockets.ws_manager import ws_manager
from app.adapters.pytorch_adapter import PyTorchAdapter
from app.adapters.tensorflow_adapter import TensorFlowAdapter
from app.adapters.yolo_adapter import YOLOAdapter
from app.domain.schemas.telemetry_schema import MetricData, TelemetryData
from app.automation.action_executor import action_executor, ExecutionContext

logger = logging.getLogger(__name__)

class ActiveTrainingSession:
    def __init__(self, session_id: str, project_id: str, pm: WindowsProcessManager, adapter: Any):
        self.session_id = session_id
        self.project_id = project_id
        self.pm = pm
        self.adapter = adapter
        self.status = "RUNNING"
        self.gpu_state = "Active"
        self.pid: Optional[int] = None
        self.telemetry_task: Optional[asyncio.Task] = None
        self.metrics_history: List[Dict[str, Any]] = []
        self.logs_history: List[str] = []

class TrainingManager:
    def __init__(self):
        self.active_sessions: Dict[str, ActiveTrainingSession] = {}
        self.collector = SystemCollector()

    def get_adapter_for_framework(self, framework: str):
        fw = framework.lower()
        if "pytorch" in fw or "torch" in fw:
            return PyTorchAdapter()
        elif "tensorflow" in fw or "tf" in fw:
            return TensorFlowAdapter()
        elif "yolo" in fw or "ultralytics" in fw:
            return YOLOAdapter()
        else:
            return PyTorchAdapter()

    async def start_training(self, project_id: UUID, session_name: Optional[str] = None, hyperparameters: Optional[Dict[str, Any]] = None, extra_args: Optional[List[str]] = None) -> Dict[str, Any]:
        async with AsyncSessionLocal() as db:
            proj_repo = ProjectRepository(db)
            session_repo = SessionRepository(db)

            logger.info(f"[STEP 2/6] Loading project from database for ID: {project_id}")
            project = await proj_repo.get_by_id(project_id)
            if not project:
                raise ValueError(f"Project with ID '{project_id}' not found.")

            adapter = self.get_adapter_for_framework(project.framework)

            # Resolve script path
            script_path = project.training_script_path
            if script_path and not os.path.isabs(script_path):
                root_candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", script_path))
                if os.path.exists(root_candidate):
                    script_path = root_candidate

            # Validate environment & training script
            logger.info(f"[STEP 3/6] Validating environment and project paths: script_path='{script_path}'")
            val_res = adapter.validate_environment(script_path)
            if not val_res.is_valid:
                raise ValueError(f"Environment validation failed: {'; '.join(val_res.errors)}")

            # Ensure output and checkpoint directories exist
            output_dir = project.output_dir or "./storage/outputs"
            checkpoint_dir = project.checkpoint_dir or "./storage/checkpoints"
            if not os.path.isabs(output_dir):
                output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", output_dir))
            if not os.path.isabs(checkpoint_dir):
                checkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", checkpoint_dir))

            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(checkpoint_dir, exist_ok=True)
            logger.info(f"Verified working directories. Output: '{output_dir}', Checkpoint: '{checkpoint_dir}'")

            # Create session record in DB
            s_name = session_name or f"Run-{project.name}-{project_id.hex[:6]}"
            session_obj = await session_repo.create_session(
                project_id=project_id,
                session_name=s_name,
                hyperparameters=hyperparameters or {}
            )
            session_id_str = str(session_obj.id)
            await session_repo.update_status(session_obj.id, "STARTING")
            await ws_manager.broadcast_to_session(session_id_str, {
                "type": "STATUS_UPDATE",
                "session_id": session_id_str,
                "status": "STARTING"
            })

            # Build launch command
            cmd = adapter.build_launch_command(
                script_path=script_path,
                hyperparameters=hyperparameters or {},
                extra_args=extra_args
            )

            pm = WindowsProcessManager(session_id=session_id_str)
            active_run = ActiveTrainingSession(
                session_id=session_id_str,
                project_id=str(project_id),
                pm=pm,
                adapter=adapter
            )
            self.active_sessions[session_id_str] = active_run

            # Callbacks for stdout & stderr streams
            async def on_stdout(line: str):
                logger.info(f"[{session_id_str[:8]}] stdout: {line}")
                active_run.logs_history.append(line)
                
                # Push console log line to WebSocket clients
                await ws_manager.broadcast_to_session(session_id_str, {
                    "type": "CONSOLE_LOG",
                    "session_id": session_id_str,
                    "stream": "stdout",
                    "line": line
                })

                # Store log in database
                try:
                    async with AsyncSessionLocal() as log_db:
                        l_repo = SessionRepository(log_db)
                        await l_repo.add_log_line(session_obj.id, "stdout", line)
                except Exception as e:
                    logger.error(f"Error persisting stdout log to DB: {e}")

                # Parse metrics
                parsed = adapter.parse_stdout_line(line)
                if parsed:
                    active_run.metrics_history.append(parsed.model_dump())
                    try:
                        async with AsyncSessionLocal() as metric_db:
                            m_repo = SessionRepository(metric_db)
                            await m_repo.add_metric(session_obj.id, parsed)
                    except Exception as e:
                        logger.error(f"Error persisting metric to DB: {e}")

                    # Push metric update to WebSocket
                    await ws_manager.broadcast_to_session(session_id_str, {
                        "type": "METRIC_UPDATE",
                        "session_id": session_id_str,
                        "metric": parsed.model_dump()
                    })

            async def on_stderr(line: str):
                logger.warning(f"[{session_id_str[:8]}] stderr: {line}")
                active_run.logs_history.append(line)
                await ws_manager.broadcast_to_session(session_id_str, {
                    "type": "CONSOLE_LOG",
                    "session_id": session_id_str,
                    "stream": "stderr",
                    "line": line
                })
                try:
                    async with AsyncSessionLocal() as log_db:
                        l_repo = SessionRepository(log_db)
                        await l_repo.add_log_line(session_obj.id, "stderr", line)
                except Exception as e:
                    logger.error(f"Error persisting stderr log to DB: {e}")

            # Start process
            logger.info(f"[STEP 4/6] Spawning training subprocess: {' '.join(cmd)}")
            pid = await pm.start_process(
                command=cmd,
                cwd=output_dir,
                stdout_callback=on_stdout,
                stderr_callback=on_stderr
            )
            active_run.pid = pid
            logger.info(f"[STEP 5/6] Process spawned with PID: {pid}. Streaming logs & telemetry...")

            await session_repo.update_status(session_obj.id, "RUNNING", pid=pid)
            await ws_manager.broadcast_to_session(session_id_str, {
                "type": "STATUS_UPDATE",
                "session_id": session_id_str,
                "status": "RUNNING",
                "pid": pid
            })

            # Start 1Hz hardware telemetry background task
            active_run.telemetry_task = asyncio.create_task(self._poll_telemetry(session_id_str, session_obj.id, pid))

            return {
                "session_id": session_id_str,
                "project_id": str(project_id),
                "session_name": s_name,
                "status": "RUNNING",
                "pid": pid
            }

    async def _poll_telemetry(self, session_id_str: str, session_uuid: UUID, pid: int):
        """1Hz background task recording hardware metrics and broadcasting via WS."""
        logger.info(f"Started 1Hz hardware telemetry polling for session {session_id_str}")
        while session_id_str in self.active_sessions:
            active_run = self.active_sessions[session_id_str]
            if active_run.status not in ["RUNNING", "PAUSED"]:
                break

            # Collect metrics
            telem = self.collector.collect(pid=pid)

            # Collect metrics
            telem = self.collector.collect(pid=pid)
            telem["gpu_state"] = active_run.gpu_state

            # Save to database
            try:
                async with AsyncSessionLocal() as db:
                    repo = SessionRepository(db)
                    telem_schema = TelemetryData(**telem)
                    await repo.add_telemetry(session_uuid, telem_schema)
            except Exception as e:
                logger.error(f"Error persisting telemetry for session {session_id_str}: {e}")

            # Broadcast via WebSocket
            await ws_manager.broadcast_to_session(session_id_str, {
                "type": "TELEMETRY_UPDATE",
                "session_id": session_id_str,
                "telemetry": telem
            })

            # Check if process finished
            if active_run.pm.process and active_run.pm.process.poll() is not None:
                exit_code = active_run.pm.process.poll()
                final_status = "COMPLETED" if exit_code == 0 else "FAILED"
                logger.info(f"Process for session {session_id_str} exited with code {exit_code} ({final_status})")
                
                active_run.status = final_status
                active_run.gpu_state = "Released"

                async with AsyncSessionLocal() as db:
                    repo = SessionRepository(db)
                    await repo.update_status(session_uuid, final_status, exit_code=exit_code)

                # Push completion and GPU Released events
                await ws_manager.broadcast_to_session(session_id_str, {
                    "type": "CONSOLE_LOG",
                    "session_id": session_id_str,
                    "stream": "stdout",
                    "line": f"[INFO] Training Finished with status '{final_status}'. GPU Released & VRAM Cleared."
                })

                await ws_manager.broadcast_to_session(session_id_str, {
                    "type": "GPU_RELEASED",
                    "session_id": session_id_str,
                    "gpu_state": "Released"
                })

                await ws_manager.broadcast_to_session(session_id_str, {
                    "type": "STATUS_UPDATE",
                    "session_id": session_id_str,
                    "status": final_status,
                    "exit_code": exit_code
                })

                # If training completed successfully, save model, release GPU, and trigger 30s auto shutdown countdown dialog
                if final_status == "COMPLETED":
                    logger.info(f"Training completed successfully. Saving final model & scheduling Auto Shutdown Confirmation Dialog (30s)...")
                    ctx = ExecutionContext(
                        session_id=session_id_str,
                        project_id=active_run.project_id,
                        output_dir="./storage/outputs",
                        checkpoint_dir="./storage/checkpoints"
                    )
                    await action_executor.execute_action("SAVE_BEST_MODEL", {}, ctx)
                    await action_executor.execute_action("SYSTEM_SHUTDOWN", {"grace_period_sec": 30}, ctx)

                break

            await asyncio.sleep(1.0)

    async def pause_training(self, session_id: str) -> bool:
        active_run = self.active_sessions.get(session_id)
        if not active_run:
            return False
        success = await active_run.pm.pause_process()
        if success:
            active_run.status = "PAUSED"
            async with AsyncSessionLocal() as db:
                repo = SessionRepository(db)
                await repo.update_status(UUID(session_id), "PAUSED")
            await ws_manager.broadcast_to_session(session_id, {"type": "STATUS_UPDATE", "session_id": session_id, "status": "PAUSED"})
        return success

    async def resume_training(self, session_id: str) -> bool:
        active_run = self.active_sessions.get(session_id)
        if not active_run:
            return False
        success = await active_run.pm.resume_process()
        if success:
            active_run.status = "RUNNING"
            async with AsyncSessionLocal() as db:
                repo = SessionRepository(db)
                await repo.update_status(UUID(session_id), "RUNNING")
            await ws_manager.broadcast_to_session(session_id, {"type": "STATUS_UPDATE", "session_id": session_id, "status": "RUNNING"})
        return success

    async def stop_training(self, session_id: str) -> int:
        active_run = self.active_sessions.get(session_id)
        if not active_run:
            return -1
        exit_code = await active_run.pm.stop_process()
        active_run.status = "CANCELLED"
        async with AsyncSessionLocal() as db:
            repo = SessionRepository(db)
            await repo.update_status(UUID(session_id), "CANCELLED", exit_code=exit_code)

        await ws_manager.broadcast_to_session(session_id, {"type": "STATUS_UPDATE", "session_id": session_id, "status": "CANCELLED", "exit_code": exit_code})
        self.active_sessions.pop(session_id, None)
        return exit_code

    async def kill_process(self, session_id: str) -> bool:
        active_run = self.active_sessions.get(session_id)
        if not active_run:
            return False
        exit_code = await active_run.pm.stop_process()
        active_run.status = "CANCELLED"
        active_run.gpu_state = "Released"
        async with AsyncSessionLocal() as db:
            repo = SessionRepository(db)
            await repo.update_status(UUID(session_id), "CANCELLED", exit_code=exit_code)

        await ws_manager.broadcast_to_session(session_id, {"type": "STATUS_UPDATE", "session_id": session_id, "status": "CANCELLED", "exit_code": exit_code})
        await ws_manager.broadcast_to_session(session_id, {"type": "GPU_RELEASED", "session_id": session_id, "gpu_state": "Released"})
        await ws_manager.broadcast_to_session(session_id, {"type": "CONSOLE_LOG", "session_id": session_id, "stream": "stdout", "line": "[INFO] Process force killed. GPU Released."})
        self.active_sessions.pop(session_id, None)
        return True

    async def release_gpu(self, session_id: str) -> bool:
        active_run = self.active_sessions.get(session_id)
        if active_run:
            active_run.gpu_state = "Released"
        await ws_manager.broadcast_to_session(session_id, {"type": "GPU_RELEASED", "session_id": session_id, "gpu_state": "Released"})
        await ws_manager.broadcast_to_session(session_id, {"type": "CONSOLE_LOG", "session_id": session_id, "stream": "stdout", "line": "[INFO] Manual GPU Resource Release Triggered. VRAM Cleared & Allocated State Released."})
        return True

    async def restart_training(self, session_id: str) -> Dict[str, Any]:
        active_run = self.active_sessions.get(session_id)
        proj_id = active_run.project_id if active_run else None

        if active_run:
            await self.stop_training(session_id)

        if not proj_id:
            async with AsyncSessionLocal() as db:
                repo = SessionRepository(db)
                sess = await repo.get_by_id(UUID(session_id))
                if not sess:
                    raise ValueError(f"Session '{session_id}' not found.")
                proj_id = str(sess.project_id)

        return await self.start_training(project_id=UUID(proj_id))

training_manager = TrainingManager()
