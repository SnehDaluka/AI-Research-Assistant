from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.api.routers import (
    health,
    sessions,
    chat,
    documents,
    auth,
)

app = FastAPI(
    title="AI Research Assistant",
    description="Local RAG-based AI Research Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(auth.router)

# Mount frontend if it exists
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")