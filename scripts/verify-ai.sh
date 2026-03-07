#!/bin/bash
set -e

curl -fsS http://localhost:8000/health >/dev/null
curl -fsS http://localhost:11434/api/tags >/dev/null
echo "AI reasoning services are reachable"
