from collections.abc import Callable

_AGENTS: dict[str, object] = {}

def register_agent(name: str, agent: object) -> None:
    if not name.strip():
        raise ValueError("agent name must not be empty")
    _AGENTS[name] = agent

def get_agent(name: str) -> object:
    return _AGENTS[name]

def list_agents() -> list[str]:
    return sorted(_AGENTS)
