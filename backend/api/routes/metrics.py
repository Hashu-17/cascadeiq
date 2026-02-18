from fastapi import APIRouter
from observability.metrics import snapshot_metrics

router = APIRouter(prefix="/metrics", tags=["observability"])

@router.get("")
def metrics():
    return snapshot_metrics()
