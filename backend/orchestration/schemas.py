from datetime import datetime
from pydantic import BaseModel

class WorkflowStateResponse(BaseModel):
    workflow_id: str
    incident_id: str
    status: str
    updated_at: datetime
