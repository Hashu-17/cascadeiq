from ai.contracts import IncidentDescription
from ai.prompts import DESCRIPTION_PROMPT

def generate_description(model, context: dict) -> IncidentDescription:
    structured = model.with_structured_output(IncidentDescription)
    return structured.invoke(DESCRIPTION_PROMPT.format(**context))
