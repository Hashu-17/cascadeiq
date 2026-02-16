from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from database import Base

class ExecutionTraceModel(Base):
    __tablename__ = "execution_traces"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String, index=True)
    stage = Column(String, index=True)
    status = Column(String, default="completed")
    message = Column(Text)
    agent_name = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
