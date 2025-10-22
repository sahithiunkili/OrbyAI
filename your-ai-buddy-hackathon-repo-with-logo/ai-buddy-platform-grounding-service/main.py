from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="ai-buddy-platform-grounding-service")

class Health(BaseModel):
    status: str = "ok"
    service: str = "ai-buddy-platform-grounding-service"

@app.get("/health")
def health():
    return Health().model_dump()

@app.get("/spec")
def spec():
    return {"service": "ai-buddy-platform-grounding-service", "description": "Stub for hackathon MVP. Replace with real logic."}
