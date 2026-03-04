class AIAnalysisError(RuntimeError):
  """Raised when required AI reasoning cannot complete."""


def format_ai_error(exc: Exception) -> str:
  return f"{type(exc).__name__}: {exc}"
