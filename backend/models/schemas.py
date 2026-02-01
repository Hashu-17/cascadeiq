from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class IncidentCreate(BaseModel):
    service_name: str
    severity: str = "MEDIUM"
    incident_type: str
    raw_logs: str
    timestamp: Optional[datetime] = None
    incident_metadata: dict = Field(default_factory=dict)
    description: Optional[str] = None

class IncidentResponse(BaseModel):
    id: int
    incident_id: str
    service_name: str
    severity: str
    incident_type: Optional[str] = None
    status: str
    description: Optional[str] = None
    raw_logs: Optional[str] = None
    incident_timestamp: Optional[datetime] = None
    incident_metadata: Optional[dict] = None
    workflow_id: Optional[str] = None
    workflow_status: Optional[str] = None
    probable_cause: Optional[str] = None
    confidence: Optional[float] = None
    analysis_severity: Optional[str] = None
    analysis_summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class WorkflowResponse(BaseModel):
    id: int
    workflow_id: str
    incident_id: str
    status: str
    probable_cause: Optional[str] = None
    confidence: Optional[float] = None
    analysis_severity: Optional[str] = None
    analysis_summary: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
