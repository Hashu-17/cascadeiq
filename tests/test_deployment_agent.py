from agents.contracts import AgentInput
from agents.deployment_agent import DeploymentAgent

def test_deployment_agent_reports_version():
    result = DeploymentAgent().analyze(AgentInput(incident_id='1', service_name='api', incident_type='deploy', metadata={'version': '1.2.0'}))
    assert result.agent_name == 'deployment-agent'
    assert '1.2.0' in result.evidence[0]
