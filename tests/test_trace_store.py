from observability.trace_store import TraceStore

def test_trace_store_exposes_workflow_query():
    assert hasattr(TraceStore, 'list_for_workflow')
