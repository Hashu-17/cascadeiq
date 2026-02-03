from datetime import datetime, timezone
from typing import Dict, Any

def generate_incident_from_scenario(scenario: str) -> Dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    scenarios = {
        "api-failure": {
            "service_name": "payment-service",
            "severity": "HIGH",
            "incident_type": "API_TIMEOUT",
            "description": "API request timeout detected",
            "raw_logs": "sample log",
            "timestamp": timestamp,
            "incident_metadata": {},
        }
    }
    if scenario not in scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")
    return scenarios[scenario]
