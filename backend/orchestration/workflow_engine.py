import uuid
from datetime import datetime
from backend.orchestration.state import WorkflowState
from backend.orchestration.state_manager import save_state

def initialize_workflow(incident_id: str) -> WorkflowState:
    state = WorkflowState(
        workflow_id=str(uuid.uuid4()),
        incident_id=incident_id,
        status='INITIALIZED',
        updated_at=datetime.utcnow(),
    )
    save_state(state)
    return state

# Initialization hooks
