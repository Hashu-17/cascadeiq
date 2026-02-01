from datetime import datetime
import os
from sqlalchemy import Column, DateTime, Float, Integer, JSON, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cascadeiq:cascadeiq_dev@localhost:5432/cascadeiq")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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
    incident_timestamp = Column(DateTime, default=datetime.utcnow)
    incident_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True)
    incident_id = Column(String, index=True)
    status = Column(String, default="INITIALIZED")
    probable_cause = Column(String)
    confidence = Column(Float)
    analysis_severity = Column(String)
    analysis_summary = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
