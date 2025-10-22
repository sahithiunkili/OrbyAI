from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="ai-buddy-platform-assignment-tracker")

class Health(BaseModel):
    status: str = "ok"
    service: str = "ai-buddy-platform-assignment-tracker"

@app.get("/health")
def health():
    return Health().model_dump()

@app.get("/spec")
def spec():
    return {"service": "ai-buddy-platform-assignment-tracker", "description": "Stub for hackathon MVP. Replace with real logic."}
