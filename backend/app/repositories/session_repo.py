from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime

from app.domain.models.models import TrainingSession, Metric, SystemTelemetry
from app.domain.schemas.telemetry_schema import MetricData, TelemetryData

class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, project_id: UUID, session_name: str, hyperparameters: Dict[str, Any]) -> TrainingSession:
        db_obj = TrainingSession(
            project_id=project_id,
            session_name=session_name,
            status="INITIALIZING",
            hyperparameters=hyperparameters
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, session_id: UUID) -> Optional[TrainingSession]:
        result = await self.session.execute(select(TrainingSession).where(TrainingSession.id == session_id))
        return result.scalars().first()

    async def update_status(self, session_id: UUID, status: str, pid: Optional[int] = None, exit_code: Optional[int] = None) -> Optional[TrainingSession]:
        db_obj = await self.get_by_id(session_id)
        if not db_obj:
            return None
        db_obj.status = status
        if pid is not None:
            db_obj.pid = pid
        if exit_code is not None:
            db_obj.exit_code = exit_code
        if status == "RUNNING" and not db_obj.start_time:
            db_obj.start_time = datetime.now()
        elif status in ["COMPLETED", "FAILED", "CANCELLED"]:
            db_obj.end_time = datetime.now()
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def add_metric(self, session_id: UUID, metric_data: MetricData) -> Metric:
        db_obj = Metric(
            session_id=session_id,
            epoch=metric_data.epoch,
            step=metric_data.step,
            loss=metric_data.loss,
            val_loss=metric_data.val_loss,
            accuracy=metric_data.accuracy,
            learning_rate=metric_data.learning_rate,
            step_time_ms=metric_data.step_time_ms
        )
        self.session.add(db_obj)
        await self.session.commit()
        return db_obj

    async def add_telemetry(self, session_id: UUID, telem_data: TelemetryData) -> SystemTelemetry:
        db_obj = SystemTelemetry(
            session_id=session_id,
            **telem_data.model_dump()
        )
        self.session.add(db_obj)
        await self.session.commit()
        return db_obj

    async def add_log_line(self, session_id: UUID, stream: str, log_line: str) -> SessionLog:
        db_obj = SessionLog(
            session_id=session_id,
            stream=stream,
            log_line=log_line
        )
        self.session.add(db_obj)
        await self.session.commit()
        return db_obj

    async def get_session_metrics(self, session_id: UUID, limit: int = 500) -> List[Metric]:
        result = await self.session.execute(
            select(Metric).where(Metric.session_id == session_id).order_by(Metric.timestamp.asc()).limit(limit)
        )
        return list(result.scalars().all())

    async def get_session_telemetry(self, session_id: UUID, limit: int = 500) -> List[SystemTelemetry]:
        result = await self.session.execute(
            select(SystemTelemetry).where(SystemTelemetry.session_id == session_id).order_by(SystemTelemetry.timestamp.asc()).limit(limit)
        )
        return list(result.scalars().all())
