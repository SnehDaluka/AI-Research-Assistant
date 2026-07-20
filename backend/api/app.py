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
    title="AI Research Assistant API",
    description="""
    API for the AI Research Assistant.
    
    ## Authentication
    Most endpoints are protected by JWT. You can obtain a JWT token by logging in via Google at the `/auth/google` endpoint. 
    Once you have the token, click the **Authorize** button below and enter it to test the API directly from this Swagger interface!
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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