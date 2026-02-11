from agents.contracts import AgentInput
from agents.log_agent import LogAgent

def test_log_agent_detects_redis_failure():
    result = LogAgent().analyze(AgentInput(
        incident_id="test-1",
        service_name="payment-service",
        incident_type="API_TIMEOUT",
        raw_logs="redis timeout while processing payment",
    ))
    assert result.agent_name == "log-agent"
    assert result.confidence > 0.7
    assert "Redis" in result.probable_cause
