from pydantic import BaseModel

class DeploymentEvidence(BaseModel):
    version: str
    deployed_at: str | None = None
    changed_files: list[str] = []
