from datetime import datetime
from agents.contracts import AgentHypothesis, AgentInput

class LogAgent:
    name = "log-agent"

    def analyze(self, payload: AgentInput) -> AgentHypothesis:
        text = f"{payload.raw_logs} {payload.incident_type}".lower()
        evidence = []
        cause = "Unknown operational failure"
        confidence = 0.5

        rules = [
            ("redis", "Redis timeout or connectivity issue", 0.82),
            ("timeout", "Upstream timeout", 0.74),
            ("database", "Database connection issue", 0.78),
            ("payment", "Payment processing failure", 0.70),
        ]
        for keyword, candidate, score in rules:
            if keyword in text:
                cause = candidate
                confidence = score
                evidence.append(f"matched keyword: {keyword}")
                break

        return AgentHypothesis(
            agent_name=self.name,
            probable_cause=cause,
            confidence=confidence,
            evidence=evidence,
            recommendation="Inspect the affected dependency and recent errors.",
            analyzed_at=datetime.utcnow(),
        )

# Log signal extraction remains deterministic for local development.
