#!/bin/bash
set -e

curl -fsS http://localhost:8000/health >/dev/null
curl -fsS http://localhost:8000/metrics >/dev/null
curl -fsS http://localhost:9090/-/healthy >/dev/null
echo "Phase 4 observability checks passed"
