from agents.contracts import AgentHypothesis

def validate_hypothesis(result: AgentHypothesis) -> AgentHypothesis:
    if not result.probable_cause.strip():
        raise ValueError("probable cause must not be empty")
    return result
