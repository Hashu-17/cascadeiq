from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WorkflowState:
    workflow_id: str
    incident_id: str
    status: str
    probable_cause: Optional[str] = None
    confidence: Optional[float] = None
    analysis_severity: Optional[str] = None
    analysis_summary: Optional[str] = None
    updated_at: datetime
