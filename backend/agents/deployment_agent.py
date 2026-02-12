from datetime import datetime
from agents.contracts import AgentHypothesis, AgentInput

class DeploymentAgent:
    name = "deployment-agent"

    def analyze(self, payload: AgentInput) -> AgentHypothesis:
        version = payload.metadata.get("version", "unknown")
        return AgentHypothesis(
            agent_name=self.name,
            probable_cause="Recent deployment may have changed service behavior",
            confidence=0.58 if version != "unknown" else 0.42,
            evidence=[f"deployment version: {version}"],
            recommendation="Compare the deployment with the previous release.",
            analyzed_at=datetime.utcnow(),
        )
