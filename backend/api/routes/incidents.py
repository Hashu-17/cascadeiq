import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import Incident, get_db
from backend.models.schemas import IncidentCreate, IncidentResponse

router = APIRouter(prefix="/api", tags=["incidents"])

@router.post("/incident", response_model=IncidentResponse)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(
        incident_id=str(uuid.uuid4()),
        service_name=payload.service_name,
        severity=payload.severity,
        description=payload.description,
        status="ACTIVE",
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident
from fastapi import HTTPException

@router.get("/incidents", response_model=list[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@router.get("/incident/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident
