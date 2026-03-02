from langchain_ollama import ChatOllama
from ai.settings import settings


def create_model() -> ChatOllama:
  return ChatOllama(
    model=settings.model,
    base_url=settings.ollama_base_url,
    temperature=0,
    timeout=settings.timeout_seconds,
  )
