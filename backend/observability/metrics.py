from collections import Counter
from threading import Lock

_lock = Lock()
_requests = Counter()
_durations: list[float] = []

def record_request(route: str, duration_ms: float, status_code: int) -> None:
    with _lock:
        _requests[f"{status_code}:{route}"] += 1
        _durations.append(duration_ms)

def snapshot_metrics() -> dict:
    with _lock:
        average = sum(_durations) / len(_durations) if _durations else 0.0
        return {
            "requests": dict(_requests),
            "request_count": sum(_requests.values()),
            "average_duration_ms": round(average, 2),
        }
