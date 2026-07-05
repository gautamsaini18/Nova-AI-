"""
Nova AI — FastAPI Application Entry Point
Main server with all routers, middleware, and lifecycle events.
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from backend.core.config import settings
from backend.core.logging_config import NovaLogger, setup_logging
from backend.core.rate_limiter import RateLimitMiddleware
from backend.database.session import init_db, close_db

# Initialize logging first
setup_logging()
logger = NovaLogger("main")

# Import routers
from backend.api.admin import router as admin_router
from backend.api.auth import router as auth_router
from backend.api.calculator import router as calculator_router
from backend.api.chat import router as chat_router
from backend.api.memory import router as memory_router
from backend.api.settings_api import router as settings_router
from backend.api.timer import router as timer_router
from backend.api.voice import router as voice_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: startup and shutdown events."""
    logger.info(
        "Nova AI starting up",
        version=settings.APP_VERSION,
        env=settings.APP_ENV,
    )
    await init_db()
    yield
    await close_db()
    logger.info("Nova AI shutting down gracefully")


# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Next-generation AI Voice Assistant — comparable to Siri, Alexa, and Google Assistant",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(RateLimitMiddleware)


@app.middleware("http")
async def request_timing_middleware(request: Request, call_next):
    """Log request timing for performance monitoring."""
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "Request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round(duration_ms, 2),
    )
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
    return response


# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(calculator_router, prefix="/api/v1/calculator", tags=["Calculator"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(memory_router, prefix="/api/v1/memory", tags=["Memory"])
app.include_router(settings_router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(timer_router, prefix="/api/v1/timer", tags=["Timer"])
app.include_router(voice_router, prefix="/api/v1/voice", tags=["Voice"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "Welcome to Nova AI — Your Intelligent Voice Assistant",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


# ── Global Exception Handler ──────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", path=request.url.path, error=str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred.",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
    )
