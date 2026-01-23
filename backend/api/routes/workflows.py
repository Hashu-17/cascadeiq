from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import Workflow, get_db
from backend.models.schemas import WorkflowResponse

router = APIRouter(prefix="/api", tags=["workflows"])

@router.get("/workflows", response_model=list[WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)):
    return db.query(Workflow).all()
