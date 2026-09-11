import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, BigInteger, Float, Double,
    ForeignKey, DateTime, Index, JSON, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    framework = Column(String(50), nullable=False, index=True)
    model_name = Column(String(255), nullable=False)
    dataset_path = Column(Text, nullable=False)
    training_script_path = Column(Text, nullable=False)
    output_dir = Column(Text, nullable=False)
    checkpoint_dir = Column(Text, nullable=False)
    automation_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sessions = relationship("TrainingSession", back_populates="project", cascade="all, delete-orphan")
    automation_rules = relationship("AutomationRule", back_populates="project", cascade="all, delete-orphan")
    experiments = relationship("Experiment", back_populates="project", cascade="all, delete-orphan")


class Configuration(Base):
    __tablename__ = "configurations"

    key = Column(String(100), primary_key=True)
    value = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True, index=True)
    session_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="INITIALIZING", index=True)
    pid = Column(Integer, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    exit_code = Column(Integer, nullable=True)
    hyperparameters = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="sessions")
    experiment = relationship("Experiment", back_populates="sessions")
    metrics = relationship("Metric", back_populates="session", cascade="all, delete-orphan")
    telemetry = relationship("SystemTelemetry", back_populates="session", cascade="all, delete-orphan")
    detections = relationship("AIDetection", back_populates="session", cascade="all, delete-orphan")
    predictions = relationship("AIPrediction", back_populates="session", cascade="all, delete-orphan")
    recommendations = relationship("AIRecommendation", back_populates="session", cascade="all, delete-orphan")
    health_scores = relationship("AIHealthScore", back_populates="session", cascade="all, delete-orphan")
    decision_history = relationship("AIDecisionHistory", back_populates="session", cascade="all, delete-orphan")
    trends = relationship("AITrend", back_populates="session", cascade="all, delete-orphan")
    automation_history = relationship("AutomationHistory", back_populates="session", cascade="all, delete-orphan")
    action_executions = relationship("ActionExecution", back_populates="session", cascade="all, delete-orphan")
    checkpoints = relationship("Checkpoint", back_populates="session", cascade="all, delete-orphan")
    reports = relationship("ReportRecord", back_populates="session", cascade="all, delete-orphan")


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    epoch = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    loss = Column(Double, nullable=True)
    val_loss = Column(Double, nullable=True)
    accuracy = Column(Double, nullable=True)
    learning_rate = Column(Double, nullable=True)
    step_time_ms = Column(Double, nullable=True)

    session = relationship("TrainingSession", back_populates="metrics")


class SystemTelemetry(Base):
    __tablename__ = "system_telemetry"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    cpu_utilization_pct = Column(Float, nullable=False)
    ram_used_bytes = Column(BigInteger, nullable=False)
    ram_total_bytes = Column(BigInteger, nullable=False)
    gpu_utilization_pct = Column(Float, nullable=True)
    gpu_memory_used_mb = Column(Float, nullable=True)
    gpu_memory_total_mb = Column(Float, nullable=True)
    gpu_temperature_c = Column(Float, nullable=True)
    gpu_power_draw_watts = Column(Float, nullable=True)
    disk_read_bytes_sec = Column(Float, nullable=True)
    disk_write_bytes_sec = Column(Float, nullable=True)
    disk_free_space_bytes = Column(BigInteger, nullable=False)

    session = relationship("TrainingSession", back_populates="telemetry")


# --- PHASE 3 AI ENGINE ENTITIES ---

class AIDetection(Base):
    __tablename__ = "ai_detections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    detection_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="detections")


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    remaining_time_sec = Column(Float, nullable=False)
    failure_probability = Column(Float, nullable=False)
    expected_completion_time = Column(DateTime(timezone=True), nullable=True)
    memory_growth_trend = Column(String(50), nullable=False)
    speed_trend = Column(String(50), nullable=False)
    accuracy_trend = Column(String(50), nullable=False)
    loss_trend = Column(String(50), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="predictions")


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    expected_impact = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="recommendations")


class AIHealthScore(Base):
    __tablename__ = "ai_health_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    category = Column(String(20), nullable=False)
    sub_scores = Column(JSON, default=dict)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="health_scores")


class AIDecisionHistory(Base):
    __tablename__ = "ai_decision_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    epoch = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    health_score = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)
    detections_summary = Column(JSON, default=list)
    recommendations_summary = Column(JSON, default=list)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="decision_history")


class AITrend(Base):
    __tablename__ = "ai_trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False)
    moving_average_5 = Column(Float, nullable=True)
    moving_average_20 = Column(Float, nullable=True)
    slope = Column(Float, nullable=True)
    direction = Column(String(20), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="trends")


# --- PHASE 4 AUTOMATION ENGINE ENTITIES ---

class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    trigger_event = Column(String(100), nullable=False, index=True)
    conditions_json = Column(JSON, default=dict)
    actions_sequence = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="automation_rules")
    history = relationship("AutomationHistory", back_populates="rule")


class WorkflowDefinition(Base):
    __tablename__ = "workflow_definitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    steps_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AutomationHistory(Base):
    __tablename__ = "automation_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("automation_rules.id", ondelete="SET NULL"), nullable=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    trigger_event = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    executed_actions = Column(JSON, nullable=False)
    error_log = Column(Text, nullable=True)
    duration_ms = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    rule = relationship("AutomationRule", back_populates="history")
    session = relationship("TrainingSession", back_populates="automation_history")
    action_executions = relationship("ActionExecution", back_populates="history", cascade="all, delete-orphan")


class ActionExecution(Base):
    __tablename__ = "action_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    history_id = Column(UUID(as_uuid=True), ForeignKey("automation_history.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String(100), nullable=False)
    step_index = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(JSON, default=dict)
    duration_ms = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    history = relationship("AutomationHistory", back_populates="action_executions")
    session = relationship("TrainingSession", back_populates="action_executions")


class ScheduledAction(Base):
    __tablename__ = "scheduled_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String(100), nullable=False)
    params = Column(JSON, default=dict)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(String(50), default="DESKTOP")
    status = Column(String(50), default="SENT")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RollbackHistory(Base):
    __tablename__ = "rollback_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    history_id = Column(UUID(as_uuid=True), ForeignKey("automation_history.id", ondelete="CASCADE"), nullable=False)
    failed_action_type = Column(String(100), nullable=False)
    rollback_strategy = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# --- PHASE 5 CHECKPOINT & ANALYTICS ENTITIES ---

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    hyperparameters = Column(JSON, default=dict)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="experiments")
    sessions = relationship("TrainingSession", back_populates="experiment")


class Checkpoint(Base):
    __tablename__ = "checkpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    epoch = Column(Integer, nullable=False)
    step = Column(Integer, nullable=False)
    loss = Column(Double, nullable=True)
    val_loss = Column(Double, nullable=True)
    accuracy = Column(Double, nullable=True)
    model_size_bytes = Column(BigInteger, nullable=False)
    is_best = Column(Boolean, default=False)
    is_latest = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="checkpoints")


class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    report_type = Column(String(50), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TrainingSession", back_populates="reports")


class ComparisonRecord(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_a_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    session_b_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    comparison_summary = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExportRecord(Base):
    __tablename__ = "exports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("training_sessions.id", ondelete="CASCADE"), nullable=False)
    export_type = Column(String(50), default="ZIP_BUNDLE")
    file_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# --- PHASE 6 SECURITY & PRODUCTION ENTITIES ---

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default="ML_ENGINEER") # ADMIN, ML_ENGINEER, VIEWER
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(255), nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String(45), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="audit_logs")


class BackupRecord(Base):
    __tablename__ = "backups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    backup_type = Column(String(50), nullable=False) # FULL, DATABASE, CHECKPOINTS
    file_path = Column(Text, nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    status = Column(String(50), default="COMPLETED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
