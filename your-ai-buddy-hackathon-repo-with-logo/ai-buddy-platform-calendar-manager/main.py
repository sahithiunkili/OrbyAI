from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="ai-buddy-platform-calendar-manager")

class Health(BaseModel):
    status: str = "ok"
    service: str = "ai-buddy-platform-calendar-manager"

@app.get("/health")
def health():
    return Health().model_dump()

@app.get("/spec")
def spec():
    return {"service": "ai-buddy-platform-calendar-manager", "description": "Stub for hackathon MVP. Replace with real logic."}
