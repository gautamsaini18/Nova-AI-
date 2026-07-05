"""Tests for Auth API + Security."""

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.database.models import Base, User, UserSettings
from backend.database.session import engine, async_session_factory


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session():
    async with async_session_factory() as s:
        yield s


class TestPasswordHashing:
    def test_hash_and_verify(self):
        pwd = "MySecureP@ss1"
        hashed = hash_password(pwd)
        assert hashed != pwd
        assert verify_password(pwd, hashed)

    def test_wrong_password(self):
        hashed = hash_password("correct-password")
        assert not verify_password("wrong-password", hashed)

    def test_unique_hashes(self):
        h1 = hash_password("same")
        h2 = hash_password("same")
        assert h1 != h2


class TestJWT:
    def test_create_and_decode_access(self):
        token = create_access_token(subject="user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload

    def test_create_and_decode_refresh(self):
        token = create_refresh_token(subject="user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"

    def test_access_token_expiry(self):
        from datetime import timedelta
        token = create_access_token(subject="test", expires_delta=timedelta(seconds=1))
        payload = decode_token(token)
        assert payload["sub"] == "test"

    def test_invalid_token(self):
        with pytest.raises(Exception):
            decode_token("invalid-token-here")

    def test_token_with_extra_claims(self):
        token = create_access_token(subject="user-1", extra_claims={"role": "admin"})
        payload = decode_token(token)
        assert payload["role"] == "admin"


@pytest.mark.asyncio
async def test_register_and_login():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestP@ss123",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Login with same credentials
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "TestP@ss123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data

        # Wrong password
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "wrong",
        })
        assert resp.status_code == 401

        # Duplicate email
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Another",
            "email": "test@example.com",
            "password": "TestP@ss456",
        })
        assert resp.status_code == 409


@pytest.mark.asyncio
async def test_me_endpoint():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register first
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Profile Test",
            "email": "profile@example.com",
            "password": "TestP@ss123",
        })
        token = resp.json()["access_token"]

        # Get profile
        resp = await client.get("/api/v1/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "profile@example.com"
        assert data["name"] == "Profile Test"
        assert "id" in data

        # No auth
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

        # Bad token
        resp = await client.get("/api/v1/auth/me", headers={
            "Authorization": "Bearer invalid",
        })
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Refresh Test",
            "email": "refresh@example.com",
            "password": "TestP@ss123",
        })
        refresh = resp.json()["refresh_token"]

        # Refresh
        resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh,
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

        # Invalid refresh
        resp = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": "bad-token",
        })
        assert resp.status_code == 401


@pytest.mark.asyncio
async def test_password_reset():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/auth/password-reset", json={
            "email": "anyone@example.com",
        })
        assert resp.status_code == 200
        assert resp.json()["success"] is True


@pytest.mark.asyncio
async def test_logout():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Logout Test",
            "email": "logout@example.com",
            "password": "TestP@ss123",
        })
        token = resp.json()["access_token"]

        resp = await client.post("/api/v1/auth/logout", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        assert resp.json()["success"] is True


@pytest.mark.asyncio
async def test_auth_status():
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Unauthenticated
        resp = await client.get("/api/v1/auth/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["authenticated"] is False
        assert data["user"] is None

        # Authenticated
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Status Test",
            "email": "status@example.com",
            "password": "TestP@ss123",
        })
        token = resp.json()["access_token"]

        resp = await client.get("/api/v1/auth/status", headers={
            "Authorization": f"Bearer {token}",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["authenticated"] is True
        assert data["user"]["email"] == "status@example.com"
