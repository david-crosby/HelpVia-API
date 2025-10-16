"""HelpVia API - Main Application Entry Point"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, tickets
from app.core.config import settings
from app.core.database import Base, engine
from app.core.logging_config import setup_logging

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting HelpVia API...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database ready")
    yield
    logger.info("Shutting down...")
    await engine.dispose()

app = FastAPI(
    title="HelpVia API",
    description="Ticketing system API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Welcome to HelpVia API", "docs": "/docs"}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["Tickets"])
