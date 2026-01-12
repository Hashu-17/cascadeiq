@echo off
set API_URL=http://localhost:8000

echo Checking API health...
curl -s %API_URL%/health | findstr healthy

echo Checking incidents list...
curl -s %API_URL%/api/incidents > NUL

echo OK
