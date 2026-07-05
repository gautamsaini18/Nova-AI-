"""
Nova AI — Pydantic Schemas / Models
Request and response models for all API endpoints.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


# ── Shared ────────────────────────────────────────────────────────────────────

class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    language: str = "en"
    voice_id: str = "nova"
    plan: str = "free"
    created_at: datetime
    last_active: Optional[datetime] = None


# ── Chat ──────────────────────────────────────────────────────────────────────

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    conversation_id: Optional[str] = None
    user_id: str
    voice_id: str = "nova"
    stream: bool = False
    language: str = "en"


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    voice_id: str
    timestamp: datetime
    tokens_used: Optional[int] = None
    audio_url: Optional[str] = None  # If TTS was generated


class ConversationSummary(BaseModel):
    id: str
    title: str
    preview: str
    message_count: int
    created_at: datetime
    updated_at: datetime


# ── Voice ─────────────────────────────────────────────────────────────────────

class VoiceProfile(BaseModel):
    id: str
    name: str
    category: str
    gender: str
    description: str
    openai_voice: str
    elevenlabs_voice_id: Optional[str] = None
    sample_text: str
    tags: List[str]
    is_premium: bool = False


class VoiceSynthesisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice_id: str = "nova"
    speed: float = Field(default=1.0, ge=0.25, le=4.0)


class STTRequest(BaseModel):
    language: str = "en"


class STTResponse(BaseModel):
    text: str
    language: str
    confidence: Optional[float] = None
    duration_seconds: Optional[float] = None


# ── Memory ────────────────────────────────────────────────────────────────────

class MemoryEntry(BaseModel):
    id: str
    content: str
    memory_type: str
    created_at: str
    metadata: Optional[Dict[str, Any]] = None


class RememberRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    memory_type: str = Field(default="note", pattern="^(fact|preference|note|conversation)$")
    metadata: Optional[Dict[str, Any]] = None


class SearchMemoryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    memory_type: Optional[str] = None


# ── Settings ──────────────────────────────────────────────────────────────────

class UserSettings(BaseModel):
    voice_id: str = "nova"
    language: str = "en"
    speech_speed: float = 1.0
    wake_word: str = "hey nova"
    theme: str = "dark"
    notifications_enabled: bool = True
    noise_cancellation: bool = True
    auto_save_conversations: bool = True
    privacy_mode: bool = False
    timezone: str = "Asia/Kolkata"


class UpdateSettingsRequest(BaseModel):
    voice_id: Optional[str] = None
    language: Optional[str] = None
    speech_speed: Optional[float] = None
    wake_word: Optional[str] = None
    theme: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    noise_cancellation: Optional[bool] = None
    auto_save_conversations: Optional[bool] = None
    privacy_mode: Optional[bool] = None
    timezone: Optional[str] = None
