from datetime import datetime
from pydantic import BaseModel

class ExecutionTrace(BaseModel):
    workflow_id: str
    stage: str
    status: str
    message: str
    agent_name: str | None = None
    duration_ms: int | None = None
    timestamp: datetime
