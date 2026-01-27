from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, Base
from .routers import webhook, voice_logs
from . import models
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Routers
app.include_router(webhook.router, prefix="/api/v1/webhook", tags=["webhook"])
app.include_router(voice_logs.router, prefix="/api/v1/voice_logs", tags=["voice_logs"])

# Mount Static Files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve Index (Frontend)
@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')
