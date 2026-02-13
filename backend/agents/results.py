from pydantic import BaseModel, Field
from agents.contracts import AgentHypothesis

class AgentExecutionResult(BaseModel):
    incident_id: str
    hypotheses: list[AgentHypothesis] = Field(default_factory=list)
    completed_agents: list[str] = Field(default_factory=list)
    failed_agents: list[str] = Field(default_factory=list)
