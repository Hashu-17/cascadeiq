from datetime import datetime
from sqlalchemy.orm import Session
from database import ExecutionTraceModel

class TraceStore:
    def __init__(self, db: Session) -> None:
        self.db = db

    def record(self, workflow_id: str, stage: str, message: str,
               status: str = "completed", agent_name: str | None = None,
               duration_ms: int | None = None) -> ExecutionTraceModel:
        trace = ExecutionTraceModel(
            workflow_id=workflow_id,
            stage=stage,
            status=status,
            message=message,
            agent_name=agent_name,
            duration_ms=duration_ms,
            timestamp=datetime.utcnow(),
        )
        self.db.add(trace)
        self.db.flush()
        return trace

    def list_for_workflow(self, workflow_id: str) -> list[ExecutionTraceModel]:
        return (self.db.query(ExecutionTraceModel)
                .filter(ExecutionTraceModel.workflow_id == workflow_id)
                .order_by(ExecutionTraceModel.timestamp)
                .all())

# Trace writes are flushed before the workflow transaction commits.
