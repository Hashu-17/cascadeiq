import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    # Allow backend code to import root-level packages like simulations
    sys.path.append(PROJECT_ROOT)

from api.routes.incidents import router as incidents_router
from api.routes.workflows import router as workflows_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CascadeIQ", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

app.include_router(incidents_router)
app.include_router(workflows_router)
