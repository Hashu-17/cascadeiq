from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from observability.trace_store import TraceStore

router = APIRouter(prefix="/api/workflows", tags=["observability"])

@router.get("/{workflow_id}/traces")
def list_traces(workflow_id: str, db: Session = Depends(get_db)):
    return TraceStore(db).list_for_workflow(workflow_id)
