from ai.contracts import AIHypothesis, AISynthesis

def test_structured_reasoning_contracts_are_bounded():
  hypothesis = AIHypothesis(
    agent_name="log-agent",
    probable_cause="Redis timeout",
    confidence=0.82,
    recommendation="Inspect Redis connectivity.",
  )
  synthesis = AISynthesis(
    leading_agent="log-agent",
    probable_cause=hypothesis.probable_cause,
    confidence=hypothesis.confidence,
    recommendation=hypothesis.recommendation,
    analysis_summary="The log agent found the strongest supported cause.",
  )
  assert 0 <= synthesis.confidence <= 1
