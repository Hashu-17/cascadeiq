#!/bin/bash

echo "CascadeIQ Phase 1 Verification Script"
echo "======================================"

API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"

echo "Checking API health..."
curl -s $API_URL/health || echo "API not responding"

echo -e "\nVerification complete."
