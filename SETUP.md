# CascadeIQ Setup & Development Guide

## Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## Initial Setup

### Using Docker Compose (Recommended)

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Verify services are healthy**:
   ```bash
   docker-compose ps
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

### Local Development

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm start
```

## Testing

Run the verification scripts:

```bash
# On Linux/Mac
./scripts/verify-phase1.sh

# On Windows
.\scripts\verify-phase1.bat
```

## Troubleshooting

- **Port already in use**: Change ports in docker-compose.yml
- **Database connection errors**: Ensure PostgreSQL is running and healthy
- **Redis connection errors**: Ensure Redis is running and healthy
