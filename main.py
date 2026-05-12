"""Main FastAPI application for Sinhala Exam Paper Generator."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from api.routes import papers, materials, exams

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Generate Sinhala mock exam papers using RAG pipeline",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Sinhala Exam Paper Generator API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
    }


# Include routers
app.include_router(papers.router, prefix="/api/v1/papers", tags=["papers"])
app.include_router(materials.router, prefix="/api/v1/materials", tags=["materials"])
app.include_router(exams.router, prefix="/api/v1/exams", tags=["exams"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
