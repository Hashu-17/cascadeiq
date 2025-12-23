# CascadeIQ

Incident Orchestration & Workflow Management Platform

A comprehensive system for incident generation, collection, processing, and orchestration with workflow automation and real-time monitoring.

## Quick Start

```bash
docker-compose up -d
```

Then navigate to:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Architecture

- **Backend**: FastAPI with SQLAlchemy ORM
- **Frontend**: React 18 with real-time updates
- **Database**: PostgreSQL 15
- **Queue**: Redis 7
- **Containerization**: Docker & Docker Compose

## Development

See [SETUP.md](SETUP.md) for detailed setup and development instructions.
