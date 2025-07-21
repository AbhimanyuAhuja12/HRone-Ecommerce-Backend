"""
FastAPI Ecommerce Application
Main application entry point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.logging_config import setup_logging
from app.api.v1.router import api_router
from app.core.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    setup_logging()
    await connect_to_mongo()
    logging.info("Application started successfully")
    
    yield
    
    # Shutdown
    await close_mongo_connection()
    logging.info("Application shutdown complete")


app = FastAPI(
    title="Ecommerce API",
    description="A comprehensive ecommerce backend API built with FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Global exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.get("/")
async def root():
    return {"message": "Ecommerce API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
