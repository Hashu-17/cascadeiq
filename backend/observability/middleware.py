from time import perf_counter
from fastapi import Request
from observability.metrics import record_request

async def collect_request_metrics(request: Request, call_next):
    started = perf_counter()
    response = await call_next(request)
    duration_ms = (perf_counter() - started) * 1000
    record_request(request.url.path, duration_ms, response.status_code)
    return response
