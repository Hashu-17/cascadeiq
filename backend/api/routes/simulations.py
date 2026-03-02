import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Incident, get_db
from models.schemas import IncidentResponse
from api.routes.incidents import _build_incident_response
from simulations.generator import generate_incident_from_scenario
from orchestration.workflow_engine import process_workflow_incident
from incident_queue import enqueue_incident

router = APIRouter(prefix="/api/simulate", tags=["simulations"])


def _parse_timestamp(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


@router.post("/{scenario}", response_model=IncidentResponse)
async def simulate_incident(scenario: str, db: Session = Depends(get_db)) -> IncidentResponse:
    try:
        payload = generate_incident_from_scenario(scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    incident_id = str(uuid.uuid4())
    incident_timestamp = _parse_timestamp(payload.get("timestamp"))

    incident = Incident(
        incident_id=incident_id,
        service_name=payload["service_name"],
        severity=payload["severity"],
        incident_type=payload["incident_type"],
        original_description=payload["description"],
        description=payload["description"],
        raw_logs=payload["raw_logs"],
        incident_timestamp=incident_timestamp,
        incident_metadata=payload.get("incident_metadata", {}),
        status="ACTIVE",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    enqueue_incident(json.dumps({
        "incident_id": incident_id,
        "service_name": payload["service_name"],
        "timestamp": payload["timestamp"],
    }))

    workflow = process_workflow_incident(incident, db)
    return _build_incident_response(incident, workflow)
