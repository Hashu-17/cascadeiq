from datetime import datetime, timezone
import os
from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    try:
        import psycopg2  # noqa: F401
        DATABASE_URL = "postgresql://cascadeiq:cascadeiq_dev@localhost:5432/cascadeiq"
    except ImportError:
        DATABASE_URL = "sqlite:///./cascadeiq.db"

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def _utc_now():
    return datetime.now(timezone.utc)


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True)
    service_name = Column(String, index=True)
    severity = Column(String, default="MEDIUM")
    incident_type = Column(String, index=True)
    status = Column(String, default="ACTIVE")
    description = Column(String)
    raw_logs = Column(Text)
    incident_timestamp = Column(DateTime, default=_utc_now)
    incident_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=_utc_now)


class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True)
    incident_id = Column(String, index=True)
    status = Column(String, default="INITIALIZED")
    probable_cause = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    analysis_severity = Column(String, nullable=True)
    analysis_summary = Column(Text, nullable=True)
    hypotheses = Column(JSON, default=list)
    updated_at = Column(DateTime, default=_utc_now)
    created_at = Column(DateTime, default=_utc_now)


class ExecutionTraceModel(Base):
    __tablename__ = "execution_traces"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, index=True)
    stage = Column(String)
    status = Column(String, default="completed")
    message = Column(Text)
    agent_name = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=_utc_now)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_schema():
    Base.metadata.create_all(bind=engine)
    if engine.dialect.name == "postgresql":
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE workflows ADD COLUMN IF NOT EXISTS hypotheses JSON")
            )
