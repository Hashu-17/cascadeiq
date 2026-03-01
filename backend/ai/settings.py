import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AISettings:
  model: str = os.getenv("LANGGRAPH_MODEL", "qwen2.5:7b")
  ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
  timeout_seconds: float = float(os.getenv("AI_REQUEST_TIMEOUT_SECONDS", "60"))
  required: bool = os.getenv("AI_REQUIRED", "true").lower() == "true"


settings = AISettings()
