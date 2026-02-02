import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Incident, Workflow, get_db
from models.schemas import IncidentCreate, IncidentResponse
from orchestration.state_manager import WorkflowStateManager
from orchestration.workflow_engine import analyze_incident
from incident_queue import enqueue_incident

router = APIRouter(prefix="/api", tags=["incidents"])

def _build_incident_response(incident: Incident, workflow: Workflow | None) -> dict:
    response = IncidentResponse.model_validate(incident).model_dump()
    if workflow:
        response.update({
            "workflow_id": workflow.workflow_id,
            "workflow_status": workflow.status,
            "probable_cause": workflow.probable_cause,
            "confidence": workflow.confidence,
            "analysis_severity": workflow.analysis_severity,
            "analysis_summary": workflow.analysis_summary,
        })
    return response

@router.post("/incident", response_model=IncidentResponse)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident_timestamp = payload.timestamp or datetime.utcnow()
    incident = Incident(
        incident_id=str(uuid.uuid4()),
        service_name=payload.service_name,
        severity=payload.severity,
        incident_type=payload.incident_type,
        description=payload.description,
        raw_logs=payload.raw_logs,
        incident_timestamp=incident_timestamp,
        incident_metadata=payload.incident_metadata,
        status="ACTIVE",
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)

    enqueue_incident(
        json.dumps({
            "incident_id": incident.incident_id,
            "service_name": incident.service_name,
            "incident_type": incident.incident_type,
            "timestamp": incident_timestamp.isoformat(),
        })
    )

    state_manager = WorkflowStateManager(db)
    workflow = state_manager.create_workflow(incident.incident_id)
    state_manager.update_status(workflow, "INGESTION_COMPLETE")
    analysis = analyze_incident(
        raw_logs=incident.raw_logs,
        incident_type=incident.incident_type,
        service_name=incident.service_name,
        severity=incident.severity,
    )
    state_manager.apply_analysis(workflow, analysis)
    db.commit()
    db.refresh(workflow)

    return _build_incident_response(incident, workflow)

@router.get("/incidents", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()
    workflow_map = {
        workflow.incident_id: workflow
        for workflow in db.query(Workflow).all()
    }
    return [
        _build_incident_response(incident, workflow_map.get(incident.incident_id))
        for incident in incidents
    ]

@router.get("/incident/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    workflow = db.query(Workflow).filter(Workflow.incident_id == incident_id).first()
    return _build_incident_response(incident, workflow)

@router.get("/incidents/active", response_model=list[IncidentResponse])
def list_active_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).filter(Incident.status == "ACTIVE").all()
    workflow_map = {
        workflow.incident_id: workflow
        for workflow in db.query(Workflow).all()
    }
    return [
        _build_incident_response(incident, workflow_map.get(incident.incident_id))
        for incident in incidents
    ]

@router.get("/incidents/by-service/{service_name}", response_model=list[IncidentResponse])
def list_by_service(service_name: str, db: Session = Depends(get_db)):
    incidents = db.query(Incident).filter(Incident.service_name == service_name).all()
    workflow_map = {
        workflow.incident_id: workflow
        for workflow in db.query(Workflow).all()
    }
    return [
        _build_incident_response(incident, workflow_map.get(incident.incident_id))
        for incident in incidents
    ]
