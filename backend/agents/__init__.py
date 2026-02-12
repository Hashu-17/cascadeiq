from agents.registry import list_agents, register_agent
from agents.log_agent import LogAgent
register_agent('log-agent', LogAgent())
from agents.deployment_agent import DeploymentAgent
register_agent('deployment-agent', DeploymentAgent())
