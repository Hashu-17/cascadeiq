from __future__ import annotations
import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from database import Incident, Workflow
from agents.contracts import AgentInput
from agents.runner import run_all_agents
from agents.registry import list_agents
from agents.log_agent import LogAgent
from observability.trace_store import TraceStore
from orchestration.state_manager import WorkflowStateManager


def analyze_incident(raw_logs: str, incident_type: str, service_name: str, severity: str) -> dict:
    normalized_logs = (raw_logs or "").lower()
    normalized_type = (incident_type or "").lower()

    probable_cause = "Unknown operational failure"
    confidence = 0.5
    analysis_severity = severity or "MEDIUM"

    keyword_map = [
        ("redis", "Redis timeout or connectivity issue", 0.84),
        ("pool exhausted", "Database connection pool exhausted", 0.88),
        ("timeout", "Upstream network timeout", 0.76),
        ("database", "Database connection issue", 0.80),
        ("auth", "Authentication failure", 0.75),
        ("payment", "Payment processing failure", 0.72),
        ("memory", "Memory pressure or leak", 0.74),
        ("cpu", "High CPU or resource saturation", 0.71),
        ("traffic spike", "Elevated load causing service saturation", 0.70),
    ]

    for keyword, cause, score in keyword_map:
        if keyword in normalized_logs or keyword in normalized_type:
            probable_cause = cause
            confidence = score
            break

    if "fatal" in normalized_logs or "critical" in normalized_logs:
        analysis_severity = "HIGH"
    elif "warn" in normalized_logs and analysis_severity == "HIGH":
        analysis_severity = "MEDIUM"

    analysis_summary = (
        f"Heuristic analysis for {service_name}. "
        f"Detected keywords in logs/type: {incident_type}."
    )

    return {
        "probable_cause": probable_cause,
        "confidence": confidence,
        "analysis_severity": analysis_severity,
        "analysis_summary": analysis_summary,
        "analyzed_at": datetime.now(timezone.utc),
    }


def run_log_agent(payload):
    return LogAgent().analyze(payload)


def process_workflow_incident(incident: Incident, db: Session) -> Workflow:
    state_manager = WorkflowStateManager(db)
    trace_store = TraceStore(db)

    # 1. Workflow creation
    workflow = state_manager.create_workflow(incident.incident_id)
    trace_store.record(
        workflow_id=workflow.workflow_id,
        stage="ingestion",
        message=f"Incident '{incident.incident_id}' ingested for service '{incident.service_name}' ({incident.incident_type})",
        status="completed",
    )

    state_manager.update_status(workflow, "INGESTION_COMPLETE")
    trace_store.record(
        workflow_id=workflow.workflow_id,
        stage="workflow_init",
        message=f"Workflow initialized for incident {incident.incident_id}",
        status="completed",
    )

    # 2. Agent Dispatch
    registered_agents = list_agents()
    trace_store.record(
        workflow_id=workflow.workflow_id,
        stage="agent_dispatch",
        message=f"Dispatched analysis to registered agents: {', '.join(registered_agents)}",
        status="in_progress",
    )

    agent_input = AgentInput(
        incident_id=incident.incident_id,
        service_name=incident.service_name,
        incident_type=incident.incident_type,
        severity=incident.severity or "MEDIUM",
        raw_logs=incident.raw_logs or "",
        metadata=incident.incident_metadata or {},
    )

    # 3. Agent Execution with trace per agent
    start_time = time.time()
    agent_results = run_all_agents(agent_input)
    elapsed_ms = int((time.time() - start_time) * 1000)

    for hypo in agent_results.hypotheses:
        duration = max(elapsed_ms // max(len(agent_results.hypotheses), 1), 1)
        trace_store.record(
            workflow_id=workflow.workflow_id,
            stage="agent_execution",
            message=f"{hypo.agent_name} generated hypothesis: '{hypo.probable_cause}' with {int(hypo.confidence * 100)}% confidence",
            agent_name=hypo.agent_name,
            duration_ms=duration,
            status="completed",
        )

    for failed in agent_results.failed_agents:
        trace_store.record(
            workflow_id=workflow.workflow_id,
            stage="agent_execution",
            message=f"Agent '{failed}' execution failed",
            agent_name=failed,
            status="failed",
        )

    # 4. Triage & Consensus Synthesis
    sorted_hypotheses = sorted(agent_results.hypotheses, key=lambda h: h.confidence, reverse=True)
    if sorted_hypotheses:
        top_hypo = sorted_hypotheses[0]
        probable_cause = top_hypo.probable_cause
        confidence = top_hypo.confidence
        analysis_summary = (
            f"Multi-agent reasoning complete. Leading hypothesis ({top_hypo.agent_name}): "
            f"'{top_hypo.probable_cause}' ({int(top_hypo.confidence * 100)}% confidence). "
            f"Recommendation: {top_hypo.recommendation or 'Inspect service telemetry.'}"
        )
    else:
        fallback = analyze_incident(
            raw_logs=incident.raw_logs or "",
            incident_type=incident.incident_type,
            service_name=incident.service_name,
            severity=incident.severity,
        )
        probable_cause = fallback["probable_cause"]
        confidence = fallback["confidence"]
        analysis_summary = fallback["analysis_summary"]

    hypotheses_data = [
        {
            "agent_name": h.agent_name,
            "probable_cause": h.probable_cause,
            "confidence": h.confidence,
            "evidence": h.evidence,
            "recommendation": h.recommendation,
            "analyzed_at": h.analyzed_at.isoformat() if h.analyzed_at else None,
        }
        for h in sorted_hypotheses
    ]

    analysis = {
        "probable_cause": probable_cause,
        "confidence": confidence,
        "analysis_severity": incident.severity or "MEDIUM",
        "analysis_summary": analysis_summary,
        "hypotheses": hypotheses_data,
        "analyzed_at": datetime.now(timezone.utc),
    }

    state_manager.apply_analysis(workflow, analysis)
    state_manager.update_status(workflow, "TRIAGED")

    trace_store.record(
        workflow_id=workflow.workflow_id,
        stage="triage",
        message=f"Triage complete. Primary cause: '{probable_cause}' (Confidence: {int(confidence * 100)}%)",
        status="completed",
    )

    trace_store.record(
        workflow_id=workflow.workflow_id,
        stage="completion",
        message="Workflow analysis pipeline finished successfully",
        status="completed",
    )

    db.commit()
    db.refresh(workflow)
    return workflow
