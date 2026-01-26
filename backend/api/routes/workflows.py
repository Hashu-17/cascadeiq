from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import Workflow, get_db
from backend.models.schemas import WorkflowResponse

router = APIRouter(prefix="/api", tags=["workflows"])

@router.get("/workflows", response_model=list[WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).all()
@router.post("/workflows/{workflow_id}/status", response_model=WorkflowResponse)
def update_workflow_status(workflow_id: str, status: str, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.workflow_id == workflow_id).first()
    if workflow:
        workflow.status = status
        db.commit()
        db.refresh(workflow)
    return workflow
