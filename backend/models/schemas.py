from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentCreate(BaseModel):
    service_name: str
    severity: str = "MEDIUM"
    description: str

class IncidentResponse(BaseModel):
    id: int
    incident_id: str
    service_name: str
    severity: str
    status: str
    description: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class WorkflowCreate(BaseModel):
    incident_id: str

class WorkflowResponse(BaseModel):
    id: int
    workflow_id: str
    incident_id: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
