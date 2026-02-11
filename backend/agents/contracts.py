from datetime import datetime
from pydantic import BaseModel, Field

class AgentInput(BaseModel):
    incident_id: str
    service_name: str
    incident_type: str
    raw_logs: str = ""
    metadata: dict = Field(default_factory=dict)

class AgentHypothesis(BaseModel):
    agent_name: str
    probable_cause: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[str] = Field(default_factory=list)
    recommendation: str | None = None
    analyzed_at: datetime | None = None
