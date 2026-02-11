from dataclasses import dataclass

@dataclass
class AgentContext:
    incident_id: str
    workflow_id: str | None = None
    trace_id: str | None = None
