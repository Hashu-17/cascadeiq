from dataclasses import dataclass
from datetime import datetime

@dataclass
class WorkflowState:
    workflow_id: str
    incident_id: str
    status: str
    updated_at: datetime
