from backend.redis_client import get_redis_client

INCIDENT_QUEUE = 'incident_queue'

def enqueue_incident(payload: str) -> None:
    client = get_redis_client()
    client.lpush(INCIDENT_QUEUE, payload)
