"""Tests for Pydantic Schemas."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.models.schemas import (
    ChatRequest,
    ChatResponse,
    RememberRequest,
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    VoiceSynthesisRequest,
)


class TestUserSchemas:
    def test_valid_register(self):
        data = UserRegisterRequest(name="Test User", email="test@example.com", password="securepass123")
        assert data.name == "Test User"
        assert data.email == "test@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserRegisterRequest(name="Test", email="not-an-email", password="securepass123")

    def test_short_password(self):
        with pytest.raises(ValidationError):
            UserRegisterRequest(name="Test", email="test@example.com", password="short")

    def test_valid_login(self):
        data = UserLoginRequest(email="test@example.com", password="password123")
        assert data.email == "test@example.com"


class TestChatSchemas:
    def test_valid_chat_request(self):
        data = ChatRequest(message="Hello", user_id="u1")
        assert data.message == "Hello"
        assert data.voice_id == "nova"
        assert data.stream is False

    def test_empty_message(self):
        with pytest.raises(ValidationError):
            ChatRequest(message="", user_id="u1")

    def test_long_message(self):
        with pytest.raises(ValidationError):
            ChatRequest(message="x" * 8001, user_id="u1")

    def test_chat_response(self):
        data = ChatResponse(
            message="Hi there!", conversation_id="c1",
            voice_id="nova", timestamp=datetime.now(),
        )
        assert data.message == "Hi there!"


class TestVoiceSchemas:
    def test_valid_synthesis(self):
        data = VoiceSynthesisRequest(text="Hello", voice_id="maya", speed=1.5)
        assert data.text == "Hello"
        assert data.speed == 1.5

    def test_speed_limits(self):
        with pytest.raises(ValidationError):
            VoiceSynthesisRequest(text="Hi", speed=5.0)
        with pytest.raises(ValidationError):
            VoiceSynthesisRequest(text="Hi", speed=0.1)


class TestMemorySchemas:
    def test_valid_remember(self):
        data = RememberRequest(content="User likes coffee")
        assert data.content == "User likes coffee"
        assert data.memory_type == "note"

    def test_invalid_memory_type(self):
        with pytest.raises(ValidationError):
            RememberRequest(content="test", memory_type="invalid_type")

    def test_empty_content(self):
        with pytest.raises(ValidationError):
            RememberRequest(content="")
