from agents.contracts import AgentInput, AgentHypothesis
from agents.registry import get_agent
from agents.validation import validate_hypothesis

def run_agent(name: str, payload: AgentInput) -> AgentHypothesis:
    agent = get_agent(name)
    result = agent.analyze(payload)
    return validate_hypothesis(result)

class AgentExecutionError(RuntimeError):
    pass

# Agent execution trace hook
