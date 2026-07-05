"""
Nova AI — Core Configuration
Loads all environment variables and app settings using Pydantic Settings.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── App ────────────────────────────────────────────────────────────────
    APP_NAME: str = "Nova AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    SECRET_KEY: str = Field(default="change-me-in-production-use-32-chars-min")
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # ─── API Server ──────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # ─── OpenAI ─────────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_TTS_VOICE: str = "nova"
    OPENAI_STT_MODEL: str = "whisper-1"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    # ─── ElevenLabs TTS ─────────────────────────────────────────────────────
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_DEFAULT_VOICE_ID: str = "EXAVITQu4vr4xnSDxMaL"  # "Bella"

    # ─── Porcupine Wake Word ─────────────────────────────────────────────────
    PORCUPINE_ACCESS_KEY: str = ""
    WAKE_WORD: str = "hey nova"
    WAKE_WORD_SENSITIVITY: float = 0.5

    # ─── Database ───────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./nova_ai.db"
    POSTGRES_URL: Optional[str] = None
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "nova_memory"

    # ─── Firebase ───────────────────────────────────────────────────────────
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_CREDENTIALS_PATH: str = "./firebase-credentials.json"

    # ─── Auth / Security ─────────────────────────────────────────────────────
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ─── Weather ─────────────────────────────────────────────────────────────
    OPENWEATHER_API_KEY: str = ""
    DEFAULT_CITY: str = "New Delhi"
    DEFAULT_COUNTRY_CODE: str = "IN"

    # ─── News ────────────────────────────────────────────────────────────────
    NEWS_API_KEY: str = ""

    # ─── Google Services ─────────────────────────────────────────────────────
    GOOGLE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""  # Custom Search Engine ID

    # ─── Communication ───────────────────────────────────────────────────────
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    SLACK_BOT_TOKEN: str = ""
    DISCORD_BOT_TOKEN: str = ""
    TELEGRAM_BOT_TOKEN: str = ""

    # ─── Vision ──────────────────────────────────────────────────────────────
    ENABLE_CAMERA: bool = False
    CAMERA_DEVICE_INDEX: int = 0

    # ─── Smart Home ──────────────────────────────────────────────────────────
    HOMEKIT_ENABLED: bool = False
    GOOGLE_HOME_ENABLED: bool = False

    # ─── Memory / Context ────────────────────────────────────────────────────
    MAX_CONTEXT_MESSAGES: int = 20
    MAX_MEMORY_ENTRIES: int = 1000
    MEMORY_SIMILARITY_THRESHOLD: float = 0.75

    # ─── Audio ───────────────────────────────────────────────────────────────
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_CHUNK_SIZE: int = 1024
    NOISE_REDUCTION_ENABLED: bool = True

    # ─── Logging ─────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/nova_ai.log"
    LOG_ROTATION: str = "10 MB"

    # ─── Rate Limiting ────────────────────────────────────────────────────────
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    @field_validator("OPENAI_API_KEY", "ELEVENLABS_API_KEY", mode="before")
    @classmethod
    def mask_sensitive(cls, v: str) -> str:
        return v  # Store as-is; masking only in logs

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def database_url(self) -> str:
        """Return PostgreSQL URL if set, otherwise SQLite."""
        return self.POSTGRES_URL or self.DATABASE_URL


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()


settings = get_settings()
