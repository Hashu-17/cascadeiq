from ai.contracts import IncidentDescription

def test_ai_description_requires_content():
    result = IncidentDescription(description="Redis latency affected payment authorization")
    assert result.description
