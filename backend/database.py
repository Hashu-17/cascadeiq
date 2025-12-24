from datetime import datetime
import os
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cascadeiq:cascadeiq@localhost:5432/cascadeiq")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True)
    service_name = Column(String, index=True)
    severity = Column(String, default="MEDIUM")
    status = Column(String, default="ACTIVE")
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, index=True)
    incident_id = Column(String, index=True)
    status = Column(String, default="INITIALIZED")
    created_at = Column(DateTime, default=datetime.utcnow)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
