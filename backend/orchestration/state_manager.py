from datetime import datetime
from backend.orchestration.state import WorkflowState

_STATE = {}

def save_state(state: WorkflowState) -> None:
    _STATE[state.workflow_id] = state

def load_state(workflow_id: str) -> WorkflowState | None:
    return _STATE.get(workflow_id)

def touch_state(state: WorkflowState, status: str) -> WorkflowState:
    state.status = status
    state.updated_at = datetime.utcnow()
    save_state(state)
    return state
