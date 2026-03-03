from datetime import datetime, timezone

from ai.contracts import AIHypothesis, AISynthesis, IncidentDescription
from ai.prompts import DEPLOYMENT_ANALYSIS_PROMPT, DESCRIPTION_PROMPT, LOG_ANALYSIS_PROMPT, SYNTHESIS_PROMPT
from ai.state import IncidentReasoningState

def _now():
    return datetime.now(timezone.utc)

def description_node(state: IncidentReasoningState, model) -> dict:
    result = model.with_structured_output(IncidentDescription).invoke(DESCRIPTION_PROMPT.format(**state))
    return {"generated_description": result.description}

def log_analysis_node(state: IncidentReasoningState, model) -> dict:
    result = model.with_structured_output(AIHypothesis).invoke(LOG_ANALYSIS_PROMPT.format(**state, description=state["generated_description"]))
    result.agent_name = "log-agent"
    result.analyzed_at = result.analyzed_at or _now()
    return {"hypotheses": [result.model_dump()]}

def deployment_analysis_node(state: IncidentReasoningState, model) -> dict:
    result = model.with_structured_output(AIHypothesis).invoke(DEPLOYMENT_ANALYSIS_PROMPT.format(**state, description=state["generated_description"]))
    result.agent_name = "deployment-agent"
    result.analyzed_at = result.analyzed_at or _now()
    return {"hypotheses": state.get("hypotheses", []) + [result.model_dump()]}

def synthesis_node(state: IncidentReasoningState, model) -> dict:
    result = model.with_structured_output(AISynthesis).invoke(SYNTHESIS_PROMPT.format(
        context={key: state.get(key) for key in ("service_name", "incident_type", "severity", "generated_description")},
        hypotheses=state.get("hypotheses", []),
    ))
    result.analyzed_at = result.analyzed_at or _now()
    return {"synthesis": result.model_dump()}

# Log analysis is an independent graph specialist.
