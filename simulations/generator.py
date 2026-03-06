from datetime import datetime, timezone
from typing import Any


def generate_incident_from_scenario(scenario: str) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    scenarios = {
        "api-failure": {
            "service_name": "payment-service",
            "severity": "HIGH",
            "incident_type": "API_TIMEOUT",
            "description": "Payment API downstream timeout while communicating with Redis cluster",
                        "raw_logs": """ERROR [payment-service] Redis connection timeout after 3000ms
    while processing transaction authorization.
Traceback (most recent call last):
    redis.exceptions.TimeoutError: Timeout connecting to redis-cache:6379
    payment.cache.RedisClient.get_session: line 184
Request failed with HTTP 504 Gateway Timeout.""",
            "timestamp": timestamp,
            "incident_metadata": {
                "error_rate": "45%",
                "version": "v2.4.1",
                "recent_deployment": True,
                "environment": "production",
            },
        },
        "db-outage": {
            "service_name": "auth-service",
            "severity": "CRITICAL",
            "incident_type": "DB_CONNECTION_FAILURE",
            "description": "Database connection pool exhausted during authentication token verification",
                        "raw_logs": """FATAL [auth-service] database connection pool exhausted
    0 of 50 connections available in pool.
Traceback (most recent call last):
    sqlalchemy.exc.TimeoutError: QueuePool limit of 50 overflow 0 reached
    auth.persistence.TokenRepository.verify: line 91
Authentication request rejected with HTTP 503 Service Unavailable.""",
            "timestamp": timestamp,
            "incident_metadata": {
                "available_connections": 0,
                "version": "v1.9.0",
                "recent_deployment": False,
                "environment": "production",
            },
        },
        "traffic-spike": {
            "service_name": "payment-service",
            "severity": "HIGH",
            "incident_type": "HIGH_LATENCY",
            "description": "Sudden traffic surge exceeding processing capacity, increasing message queue depth",
                        "raw_logs": """WARN [payment-service] queue depth increased during traffic spike
    CPU saturation at 92%.
INFO [payment-service] current request rate: 1450 req/s (baseline: 220 req/s)
WARN [payment-service] queue depth: 18420 messages; oldest message age: 38s
ERROR [payment-service] upstream processing capacity exceeded
Request shedding enabled: 18% of incoming requests rejected.""",
            "timestamp": timestamp,
            "incident_metadata": {
                "current_rps": 1450,
                "version": "v2.4.0",
                "recent_deployment": False,
                "environment": "production",
            },
        },
    }
    if scenario not in scenarios:
        raise ValueError(f"Unknown scenario: {scenario}")
    return scenarios[scenario]

# Simulation payloads remain deterministic inputs to the AI reasoning graph.
