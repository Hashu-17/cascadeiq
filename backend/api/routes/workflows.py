from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Workflow, get_db
from models.schemas import WorkflowResponse
from observability.trace_store import TraceStore

router = APIRouter(prefix="/api", tags=["workflows"])


@router.get("/workflows", response_model=list[WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).order_by(Workflow.created_at.desc()).all()


@router.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.post("/workflows/{workflow_id}/status", response_model=WorkflowResponse)
@router.patch("/workflows/{workflow_id}/status", response_model=WorkflowResponse)
def update_workflow_status(workflow_id: str, status: str, db: Session = Depends(get_db)):
    workflow = db.query(Workflow).filter(Workflow.workflow_id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    old_status = workflow.status
    workflow.status = status.upper()
    db.commit()
    db.refresh(workflow)

    trace_store = TraceStore(db)
    trace_store.record(
        workflow_id=workflow_id,
        stage="state_transition",
        message=f"Workflow status transitioned from '{old_status}' to '{workflow.status}'",
        status="completed",
    )
    db.commit()
    return workflow
