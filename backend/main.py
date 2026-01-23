from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.incidents import router as incidents_router
from backend.api.routes.workflows import router as workflows_router
from backend.database import Base, engine

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
