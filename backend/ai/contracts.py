from datetime import datetime
from pydantic import BaseModel, Field


class IncidentDescription(BaseModel):
  description: str = Field(min_length=1)
  evidence: list[str] = Field(default_factory=list)
  analyzed_at: datetime | None = None


class AIHypothesis(BaseModel):
  agent_name: str
  probable_cause: str = Field(min_length=1)
  confidence: float = Field(ge=0, le=1)
  evidence: list[str] = Field(default_factory=list)
  recommendation: str = Field(min_length=1)
  analyzed_at: datetime | None = None


class AISynthesis(BaseModel):
  probable_cause: str = Field(min_length=1)
  confidence: float = Field(ge=0, le=1)
  recommendation: str = Field(min_length=1)
  analysis_summary: str = Field(min_length=1)
  analyzed_at: datetime | None = None
