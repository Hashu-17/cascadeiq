from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Incident
from orchestration.workflow_engine import process_workflow_incident
from observability.trace_store import TraceStore
import agents  # Ensure agents are registered


def test_process_workflow_incident_runs_agents_and_records_traces():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    incident = Incident(
        incident_id="inc-test-100",
        service_name="payment-service",
        severity="HIGH",
        incident_type="API_TIMEOUT",
        description="Redis connection timeout in payment processor",
        raw_logs="Redis connection timeout after 3000ms while authenticating token",
        incident_metadata={"version": "v2.4.1", "recent_deployment": True},
        status="ACTIVE",
    )
    session.add(incident)
    session.commit()

    workflow = process_workflow_incident(incident, session)

    assert workflow.status == "TRIAGED"
    assert workflow.probable_cause is not None
    assert "Redis" in workflow.probable_cause or "Recent deployment" in workflow.probable_cause
    assert workflow.confidence > 0.70
    assert len(workflow.hypotheses) >= 2

    # Verify hypotheses include log-agent and deployment-agent
    agent_names = [h["agent_name"] for h in workflow.hypotheses]
    assert "log-agent" in agent_names
    assert "deployment-agent" in agent_names

    # Verify traces were recorded in TraceStore
    store = TraceStore(session)
    traces = store.list_for_workflow(workflow.workflow_id)
    assert len(traces) >= 5

    stages = [t.stage for t in traces]
    assert "ingestion" in stages
    assert "workflow_init" in stages
    assert "agent_dispatch" in stages
    assert "agent_execution" in stages
    assert "triage" in stages
    assert "completion" in stages

    session.close()
