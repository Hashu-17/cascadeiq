from agents.registry import list_agents, register_agent
from agents.log_agent import LogAgent
register_agent('log-agent', LogAgent())
