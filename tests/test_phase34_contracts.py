from agents.contracts import AgentInput, AgentHypothesis
from observability.schemas import ExecutionTrace

def test_phase34_contracts_validate():
    AgentInput(incident_id='1', service_name='api', incident_type='error')
    AgentHypothesis(agent_name='log-agent', probable_cause='timeout', confidence=0.8)
    ExecutionTrace(workflow_id='w1', stage='analysis', status='completed', message='done', timestamp='2026-02-20T10:00:00')
