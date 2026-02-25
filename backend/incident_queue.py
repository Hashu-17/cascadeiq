import json
import logging
from redis_client import get_redis_client

logger = logging.getLogger(__name__)
INCIDENT_QUEUE = "incident_queue"


def enqueue_incident(payload: str) -> None:
    try:
        client = get_redis_client()
        client.lpush(INCIDENT_QUEUE, payload)
    except Exception as e:
        logger.warning("Could not enqueue incident to Redis (continuing locally): %s", e)
