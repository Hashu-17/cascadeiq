from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from database import Workflow


def _utc_now():
    return datetime.now(timezone.utc)


class WorkflowStateManager:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_workflow(self, incident_id: str) -> Workflow:
        workflow = Workflow(
            workflow_id=str(uuid.uuid4()),
            incident_id=incident_id,
            status="INITIALIZED",
            created_at=_utc_now(),
            updated_at=_utc_now(),
        )
        self.db.add(workflow)
        self.db.flush()
        return workflow

    def update_status(self, workflow: Workflow, new_status: str) -> Workflow:
        workflow.status = new_status
        workflow.updated_at = _utc_now()
        self.db.add(workflow)
        return workflow

    def apply_analysis(self, workflow: Workflow, analysis: dict) -> Workflow:
        workflow.probable_cause = analysis.get("probable_cause")
        workflow.confidence = analysis.get("confidence")
        workflow.analysis_severity = analysis.get("analysis_severity")
        workflow.analysis_summary = analysis.get("analysis_summary")
        workflow.hypotheses = analysis.get("hypotheses", [])
        workflow.updated_at = analysis.get("analyzed_at", _utc_now())
        workflow.status = "TRIAGED"
        self.db.add(workflow)
        return workflow
