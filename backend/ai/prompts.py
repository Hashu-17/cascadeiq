DESCRIPTION_PROMPT = """
Write a concise incident description from the supplied operational context.
Do not invent facts. Mention the observed symptom and its measurable impact.
Return only the requested structured fields.

Service: {service_name}
Incident type: {incident_type}
Original description: {original_description}
Raw logs:
{raw_logs}
Metadata: {metadata}
"""

LOG_ANALYSIS_PROMPT = """
Analyze the incident logs as the log analysis agent.
Identify one likely cause, cite exact signals from the input, assign calibrated
confidence from 0 to 1, and give one practical recommendation.
Never claim evidence that is not present in the input.

Service: {service_name}
Incident type: {incident_type}
Description: {description}
Raw logs:
{raw_logs}
"""

DEPLOYMENT_ANALYSIS_PROMPT = """
Analyze deployment and runtime context as the deployment correlation agent.
If deployment evidence is missing, say so and lower confidence.
Cite only supplied metadata and give one practical recommendation.

Service: {service_name}
Incident type: {incident_type}
Description: {description}
Metadata: {metadata}
"""

SYNTHESIS_PROMPT = """
Synthesize the specialist hypotheses into an incident triage decision.
Select or reconcile the strongest explanation, preserve uncertainty, cite the
available evidence, and provide one actionable recommendation.

Incident context: {context}
Specialist hypotheses: {hypotheses}
"""
