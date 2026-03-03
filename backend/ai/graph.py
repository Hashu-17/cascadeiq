from langgraph.graph import END, START, StateGraph

from ai.model import create_model
from ai.nodes import (
  deployment_analysis_node,
  description_node,
  log_analysis_node,
  synthesis_node,
)
from ai.state import IncidentReasoningState


def build_reasoning_graph():
  model = create_model()
  graph = StateGraph(IncidentReasoningState)
  graph.add_node("description", lambda state: description_node(state, model))
  graph.add_node("log_analysis", lambda state: log_analysis_node(state, model))
  graph.add_node("deployment_analysis", lambda state: deployment_analysis_node(state, model))
  graph.add_node("synthesis", lambda state: synthesis_node(state, model))
  graph.add_edge(START, "description")
  graph.add_edge("description", "log_analysis")
  graph.add_edge("log_analysis", "deployment_analysis")
  graph.add_edge("deployment_analysis", "synthesis")
  graph.add_edge("synthesis", END)
  return graph.compile()


def run_reasoning_graph(state: IncidentReasoningState) -> IncidentReasoningState:
  return build_reasoning_graph().invoke(state)
