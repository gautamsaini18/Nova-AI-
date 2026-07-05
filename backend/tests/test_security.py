"""Tests for Security Module."""

import time
from datetime import timedelta

import pytest
from jose import JWTError, jwt

from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_subject,
    hash_password,
    verify_password,
)
from backend.core.config import settings


def test_password_hashing():
    password = "MySecurePass123!"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_access_token_creation():
    user_id = "user_123"
    token = create_access_token(subject=user_id)
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "iat" in payload


def test_access_token_with_extra_claims():
    token = create_access_token(subject="user_1", extra_claims={"role": "admin"})
    payload = decode_token(token)
    assert payload["role"] == "admin"


def test_access_token_expiry():
    token = create_access_token(subject="user_1", expires_delta=timedelta(seconds=1))
    payload = decode_token(token)
    assert payload["sub"] == "user_1"
    time.sleep(2)
    with pytest.raises(JWTError):
        decode_token(token)


def test_refresh_token():
    token = create_refresh_token(subject="user_1")
    payload = decode_token(token)
    assert payload["sub"] == "user_1"
    assert payload["type"] == "refresh"


def test_get_subject_valid():
    token = create_access_token(subject="test_user")
    assert get_subject(token) == "test_user"


def test_get_subject_invalid():
    assert get_subject("invalid_token") is None


def test_token_with_integer_subject():
    token = create_access_token(subject=42)
    payload = decode_token(token)
    assert payload["sub"] == "42"
