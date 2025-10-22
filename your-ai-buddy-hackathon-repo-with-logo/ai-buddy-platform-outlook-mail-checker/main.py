from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="ai-buddy-platform-outlook-mail-checker")

class Health(BaseModel):
    status: str = "ok"
    service: str = "ai-buddy-platform-outlook-mail-checker"

@app.get("/health")
def health():
    return Health().model_dump()

@app.get("/spec")
def spec():
    return {"service": "ai-buddy-platform-outlook-mail-checker", "description": "Stub for hackathon MVP. Replace with real logic."}
