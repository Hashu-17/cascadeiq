#!/bin/bash
set -e

API_URL="http://localhost:8000"

echo "Checking API health..."
curl -s $API_URL/health | grep healthy

echo "Checking incidents list..."
curl -s $API_URL/api/incidents > /dev/null

echo "OK"
