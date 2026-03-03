from typing import Any, TypedDict


class IncidentReasoningState(TypedDict, total=False):
  incident_id: str
  service_name: str
  incident_type: str
  severity: str
  original_description: str
  raw_logs: str
  metadata: dict[str, Any]
  generated_description: str
  hypotheses: list[dict[str, Any]]
  synthesis: dict[str, Any]
  provider: str
  model: str
  error: str
