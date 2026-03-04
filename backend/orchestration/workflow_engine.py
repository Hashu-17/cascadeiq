from __future__ import annotations

import time
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ai.errors import AIAnalysisError, format_ai_error
from ai.graph import run_reasoning_graph
from ai.settings import settings
from database import Incident, Workflow
from observability.trace_store import TraceStore
from orchestration.state_manager import WorkflowStateManager


def process_workflow_incident(incident: Incident, db: Session) -> Workflow:
  state_manager = WorkflowStateManager(db)
  trace_store = TraceStore(db)
  workflow = state_manager.create_workflow(incident.incident_id)
  trace_store.record(
    workflow_id=workflow.workflow_id,
    stage="ingestion",
    message=f"Incident '{incident.incident_id}' entered AI reasoning workflow",
    status="completed",
  )
  state_manager.update_status(workflow, "AI_ANALYSIS_RUNNING")
  trace_store.record(
    workflow_id=workflow.workflow_id,
    stage="graph_start",
    message=f"Starting LangGraph reasoning with {settings.model}",
    status="in_progress",
  )

  started = time.perf_counter()
  state = {
    "incident_id": incident.incident_id,
    "service_name": incident.service_name,
    "incident_type": incident.incident_type,
    "severity": incident.severity or "MEDIUM",
    "original_description": incident.description or "",
    "raw_logs": incident.raw_logs or "",
    "metadata": incident.incident_metadata or {},
    "provider": "ollama",
    "model": settings.model,
  }
  try:
    result = run_reasoning_graph(state)
  except Exception as exc:
    message = format_ai_error(exc)
    state_manager.update_status(workflow, "AI_ANALYSIS_FAILED")
    workflow.ai_error = message
    trace_store.record(
      workflow_id=workflow.workflow_id,
      stage="graph_failure",
      message=message,
      status="failed",
      duration_ms=int((time.perf_counter() - started) * 1000),
    )
    db.commit()
    db.refresh(workflow)
    return workflow

  synthesis = result["synthesis"]
  incident.description = result["generated_description"]
  workflow.probable_cause = synthesis["probable_cause"]
  workflow.confidence = synthesis["confidence"]
  workflow.analysis_severity = incident.severity or "MEDIUM"
  workflow.analysis_summary = (
    f"Multi-agent reasoning complete. Leading hypothesis: "
    f"'{synthesis['probable_cause']}' ({int(synthesis['confidence'] * 100)}% confidence). "
    f"Recommendation: {synthesis['recommendation']}"
  )
  workflow.hypotheses = result.get("hypotheses", [])
  workflow.ai_provider = result.get("provider", "ollama")
  workflow.ai_model = result.get("model", settings.model)
  workflow.ai_error = None
  state_manager.update_status(workflow, "TRIAGED")
  trace_store.record(
    workflow_id=workflow.workflow_id,
    stage="graph_completion",
    message=f"LangGraph synthesis completed in {int((time.perf_counter() - started) * 1000)}ms",
    status="completed",
    duration_ms=int((time.perf_counter() - started) * 1000),
  )
  db.commit()
  db.refresh(workflow)
  return workflow
