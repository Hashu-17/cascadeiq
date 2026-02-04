from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Incident, get_db
from models.schemas import IncidentResponse
from simulations.generator import generate_incident_from_scenario

router = APIRouter(prefix="/api/simulate", tags=["simulations"])

@router.post("/{scenario}", response_model=IncidentResponse)
async def simulate_incident(scenario: str, db: Session = Depends(get_db)) -> IncidentResponse:
    try:
        payload = generate_incident_from_scenario(scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    incident = Incident(
        incident_id="temp",
        service_name=payload["service_name"],
        severity=payload["severity"],
        incident_type=payload["incident_type"],
        description=payload["description"],
        raw_logs=payload["raw_logs"],
        incident_metadata=payload.get("incident_metadata", {}),
        status="ACTIVE",
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return IncidentResponse.model_validate(incident)
