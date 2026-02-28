from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import List

from agents.contracts import AgentInput, AgentHypothesis
from agents.registry import get_agent, list_agents
from agents.validation import validate_hypothesis

logger = logging.getLogger(__name__)


class AgentExecutionError(RuntimeError):
    pass


@dataclass
class AgentExecutionResult:
    hypotheses: List[AgentHypothesis] = field(default_factory=list)
    failed_agents: List[str] = field(default_factory=list)


def run_agent(name: str, payload: AgentInput) -> AgentHypothesis:
    """Execute a single named agent and return a validated hypothesis."""
    agent = get_agent(name)
    result = agent.analyze(payload)
    return validate_hypothesis(result)


def run_all_agents(payload: AgentInput) -> AgentExecutionResult:
    """Execute every registered agent against the given payload.

    Returns an AgentExecutionResult containing all successful hypotheses
    and a list of agent names that raised exceptions.
    """
    result = AgentExecutionResult()
    for name in list_agents():
        try:
            hypothesis = run_agent(name, payload)
            result.hypotheses.append(hypothesis)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Agent '%s' failed: %s", name, exc)
            result.failed_agents.append(name)
    return result
