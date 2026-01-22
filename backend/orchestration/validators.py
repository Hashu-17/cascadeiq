from backend.orchestration.transitions import VALID_TRANSITIONS

def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])
