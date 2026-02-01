from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from database import Workflow

class WorkflowStateManager:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_workflow(self, incident_id: str) -> Workflow:
        workflow = Workflow(
            workflow_id=str(uuid.uuid4()),
            incident_id=incident_id,
            status="INITIALIZED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(workflow)
        self.db.flush()
        return workflow

    def update_status(self, workflow: Workflow, new_status: str) -> Workflow:
        workflow.status = new_status
        workflow.updated_at = datetime.utcnow()
        self.db.add(workflow)
        return workflow
