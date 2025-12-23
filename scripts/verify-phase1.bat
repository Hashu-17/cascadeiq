@echo off
echo CascadeIQ Phase 1 Verification Script
echo ======================================

set API_URL=http://localhost:8000
set FRONTEND_URL=http://localhost:3000

echo Checking API health...
curl -s %API_URL%/health || echo API not responding

echo.
echo Verification complete.
