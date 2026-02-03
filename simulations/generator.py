        from datetime import datetime, timezone
        from typing import Dict, Any

        def generate_incident_from_scenario(scenario: str) -> Dict[str, Any]:
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

            scenarios = {
                "api-failure": {
                    "service_name": "payment-service",
                    "severity": "HIGH",
                    "incident_type": "API_TIMEOUT",
                    "description": "API request timeout detected - payment processing delayed",
                    "raw_logs": (
                        "[2026-05-11T10:30:45.123Z] INFO: Starting payment processing request
"
                        "[2026-05-11T10:30:46.456Z] WARNING: Redis connection slow (1200ms)
"
                        "[2026-05-11T10:30:47.789Z] ERROR: Failed to connect to Redis cache
"
                        "[2026-05-11T10:30:48.012Z] ERROR: Transaction timeout after 3000ms
"
                        "[2026-05-11T10:30:48.345Z] CRITICAL: Payment service API timeout
"
                        "[2026-05-11T10:30:49.678Z] ERROR: Request failed with status 504 Gateway Timeout"
                    ),
                    "timestamp": timestamp,
                    "incident_metadata": {
                        "affected_endpoints": ["/api/process-payment"],
                        "error_rate": "45%",
                        "avg_response_time_ms": 5000,
                    },
                },
                "db-outage": {
                    "service_name": "auth-service",
                    "severity": "CRITICAL",
                    "incident_type": "DB_CONNECTION_FAILURE",
                    "description": "Database connection pool exhausted - authentication unavailable",
                    "raw_logs": (
                        "[2026-05-11T11:15:23.111Z] INFO: Auth service initialized with 50 DB connections
"
                        "[2026-05-11T11:15:24.222Z] WARNING: Database connection pool 80% utilized
"
                        "[2026-05-11T11:15:25.333Z] ERROR: Failed to acquire database connection (timeout)
"
                        "[2026-05-11T11:15:26.444Z] ERROR: Connection pool exhausted: no available connections
"
                        "[2026-05-11T11:15:27.555Z] CRITICAL: Cannot authenticate user - database unavailable
"
                        "[2026-05-11T11:15:28.666Z] ERROR: All 50 connections in use or failed"
                    ),
                    "timestamp": timestamp,
                    "incident_metadata": {
                        "pool_size": 50,
                        "available_connections": 0,
                        "pending_requests": 23,
                        "database_host": "postgres:5432",
                    },
                },
                "traffic-spike": {
                    "service_name": "payment-service",
                    "severity": "HIGH",
                    "incident_type": "HIGH_LATENCY",
                    "description": "Unusual traffic spike detected - response times degraded",
                    "raw_logs": (
                        "[2026-05-11T12:45:00.000Z] INFO: Normal traffic: 100 req/s, p95 latency 150ms
"
                        "[2026-05-11T12:45:15.100Z] WARNING: Traffic increase: 500 req/s detected
"
                        "[2026-05-11T12:45:30.200Z] WARNING: High latency: p95 = 2500ms (16x normal)
"
                        "[2026-05-11T12:45:45.300Z] ERROR: Queue depth: 1000+ pending requests
"
                        "[2026-05-11T12:46:00.400Z] CRITICAL: Traffic spike: 1200 req/s, p99 latency = 8000ms
"
                        "[2026-05-11T12:46:15.500Z] WARNING: Shedding load: rejecting 30% of requests"
                    ),
                    "timestamp": timestamp,
                    "incident_metadata": {
                        "current_rps": 1200,
                        "baseline_rps": 100,
                        "p95_latency_ms": 2500,
                        "p99_latency_ms": 8000,
                        "queue_depth": 1050,
                        "error_rate": "30%",
                    },
                },
            }

            if scenario not in scenarios:
                raise ValueError(
                    f"Unknown scenario: {scenario}. Must be one of: {', '.join(scenarios.keys())}"
                )

            return scenarios[scenario]
