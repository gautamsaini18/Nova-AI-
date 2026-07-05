"""Tests for Rate Limiting Middleware."""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from backend.core.rate_limiter import RateLimitMiddleware


class TestRateLimitMiddleware:
    @pytest.fixture
    def app(self):
        app = FastAPI()
        app.add_middleware(RateLimitMiddleware, max_requests=5, window_seconds=60)

        @app.get("/test")
        async def test_endpoint():
            return {"ok": True}

        @app.get("/health")
        async def health():
            return {"status": "healthy"}

        return app

    @pytest.fixture
    def client(self, app):
        return TestClient(app)

    def test_allows_normal_requests(self, client):
        for _ in range(5):
            resp = client.get("/test")
            assert resp.status_code == 200

    def test_blocks_excess_requests(self, client):
        for _ in range(5):
            client.get("/test")
        resp = client.get("/test")
        assert resp.status_code == 429
        data = resp.json()
        assert "retry_after_seconds" in data["detail"]
        assert "Retry-After" in resp.headers

    def test_health_endpoint_not_rate_limited(self, client):
        for _ in range(5):
            client.get("/test")
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_rate_limiter_reset(self, app, client):
        # Trigger rate limit
        for _ in range(6):
            client.get("/test")
        # Reset
        middleware = [m for m in app.user_middleware if m.cls == RateLimitMiddleware][0]
        middleware.kwargs.get("app")  # no-op
        # Actually get the instance from app
        for mw_instance in [m for m in (app.middleware_stack.__self__ if hasattr(app.middleware_stack, "__self__") else [])]:
            pass
