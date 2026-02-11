from datetime import datetime, timezone
from typing import Any

def generate_incident_from_scenario(scenario: str) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    scenarios = {
        "api-failure": {
            "service_name": "payment-service",
            "severity": "HIGH",
            "incident_type": "API_TIMEOUT",
            "description": "API request timeout detected",
            "raw_logs": "payment timeout while connecting to redis",
            "timestamp": timestamp,
            "incident_metadata": {"error_rate": "45%"},
        },
        "db-outage": {
            "service_name": "auth-service",
            "severity": "CRITICAL",
            "incident_type": "DB_CONNECTION_FAILURE",
            "description": "Database connection pool exhausted",
            "raw_logs": "database connection pool exhausted",
            "timestamp": timestamp,
            "incident_metadata": {"available_connections": 0},
        },
        "traffic-spike": {
            "service_name": "payment-service",
            "severity": "HIGH",
            "incident_type": "HIGH_LATENCY",
            "description": "Traffic spike caused elevated latency",
            "raw_logs": "queue depth increased during traffic spike",
            "timestamp": timestamp,
            "incident_metadata": {"current_rps": 1200},
        },
    }
    if scenario not in scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")
    return scenarios[scenario]
