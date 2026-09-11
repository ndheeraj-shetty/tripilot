import asyncio
import subprocess
import os
import sys
import logging
import threading
import inspect
from typing import List, Optional, Callable, Dict, Any

logger = logging.getLogger(__name__)

# Check Windows platform for PyWin32 Job Objects
IS_WINDOWS = sys.platform == "win32"
HAS_WIN32 = False
if IS_WINDOWS:
    try:
        import win32job
        import win32process
        import win32api
        import win32con
        HAS_WIN32 = True
    except ImportError:
        HAS_WIN32 = False

class WindowsProcessManager:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.process: Optional[subprocess.Popen] = None
        self.job_handle = None
        self.pid: Optional[int] = None
        self._is_paused = False

    async def start_process(
        self,
        command: List[str],
        cwd: str,
        env: Optional[Dict[str, str]] = None,
        stdout_callback: Optional[Callable[[str], Any]] = None,
        stderr_callback: Optional[Callable[[str], Any]] = None
    ) -> int:
        full_env = os.environ.copy()
        full_env["PYTHONUNBUFFERED"] = "1"
        if env:
            full_env.update(env)

        if not os.path.exists(cwd):
            logger.warning(f"Working directory '{cwd}' does not exist. Creating directory...")
            os.makedirs(cwd, exist_ok=True)

        logger.info(f"[STEP 4/6] Launching subprocess for session {self.session_id} in '{cwd}': {' '.join(command)}")

        creation_flags = win32process.CREATE_NEW_PROCESS_GROUP if (IS_WINDOWS and HAS_WIN32) else 0

        # Launch process using subprocess.Popen (compatible with all asyncio event loops)
        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            env=full_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            creationflags=creation_flags
        )

        self.pid = self.process.pid

        # Bind to Windows Job Object for clean process tree termination
        if IS_WINDOWS and HAS_WIN32 and self.pid:
            try:
                self.job_handle = win32job.CreateJobObject(None, f"ZombieRun_Job_{self.session_id}")
                extended_info = win32job.QueryInformationJobObject(
                    self.job_handle,
                    win32job.JobObjectExtendedLimitInformation
                )
                extended_info['BasicLimitInformation']['LimitFlags'] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                win32job.SetInformationJobObject(
                    self.job_handle,
                    win32job.JobObjectExtendedLimitInformation,
                    extended_info
                )
                h_process = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, self.pid)
                win32job.AssignProcessToJobObject(self.job_handle, h_process)
                win32api.CloseHandle(h_process)
            except Exception as e:
                logger.warning(f"Could not bind process {self.pid} to Windows Job Object: {e}")

        # Start thread-safe stdout & stderr line reader threads
        loop = asyncio.get_running_loop()
        if stdout_callback and self.process.stdout:
            t_out = threading.Thread(
                target=self._read_pipe_thread,
                args=(self.process.stdout, stdout_callback, loop),
                daemon=True
            )
            t_out.start()

        if stderr_callback and self.process.stderr:
            t_err = threading.Thread(
                target=self._read_pipe_thread,
                args=(self.process.stderr, stderr_callback, loop),
                daemon=True
            )
            t_err.start()

        return self.pid

    def _read_pipe_thread(self, pipe, callback: Callable[[str], Any], loop: asyncio.AbstractEventLoop):
        try:
            for line in iter(pipe.readline, ''):
                if not line:
                    break
                line_str = line.rstrip('\r\n')
                if callback:
                    if inspect.iscoroutinefunction(callback):
                        asyncio.run_coroutine_threadsafe(callback(line_str), loop)
                    else:
                        loop.call_soon_threadsafe(callback, line_str)
        except Exception as e:
            logger.error(f"Error in stream reader thread: {e}")
        finally:
            pipe.close()

    async def pause_process(self) -> bool:
        if not self.pid or self._is_paused:
            return False
        if IS_WINDOWS:
            try:
                # Suspend process threads using NtSuspendProcess / OpenProcess
                h_process = win32api.OpenProcess(win32con.PROCESS_SUSPEND_RESUME, False, self.pid)
                win32process.SuspendThread(h_process)
                win32api.CloseHandle(h_process)
                self._is_paused = True
                return True
            except Exception as e:
                logger.error(f"Failed to pause process {self.pid}: {e}")
                return False
        return False

    async def resume_process(self) -> bool:
        if not self.pid or not self._is_paused:
            return False
        if IS_WINDOWS:
            try:
                h_process = win32api.OpenProcess(win32con.PROCESS_SUSPEND_RESUME, False, self.pid)
                win32process.ResumeThread(h_process)
                win32api.CloseHandle(h_process)
                self._is_paused = False
                return True
            except Exception as e:
                logger.error(f"Failed to resume process {self.pid}: {e}")
                return False
        return False

    async def stop_process(self, timeout_sec: float = 5.0) -> int:
        if not self.process:
            return 0
        try:
            self.process.terminate()
            try:
                await asyncio.to_thread(self.process.wait, timeout=timeout_sec)
            except subprocess.TimeoutExpired:
                logger.warning(f"Process {self.pid} did not terminate in {timeout_sec}s. Killing...")
                self.process.kill()
                await asyncio.to_thread(self.process.wait)
        except Exception as e:
            logger.error(f"Error stopping process {self.pid}: {e}")

        if IS_WINDOWS and self.job_handle:
            try:
                win32api.CloseHandle(self.job_handle)
                self.job_handle = None
            except Exception:
                pass

        return self.process.returncode if self.process.returncode is not None else -1
