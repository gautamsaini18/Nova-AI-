"""
Nova AI — TTS (Text-to-Speech) Engine
Supports OpenAI TTS and ElevenLabs for voice synthesis.
"""

from __future__ import annotations

import asyncio
import io
import os
from enum import Enum
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI

from backend.core.config import settings
from backend.core.logging_config import NovaLogger
from backend.modules.voice.voice_profiles import (
    DEFAULT_VOICE_ID,
    VoiceProfile,
    get_voice_by_id,
)

logger = NovaLogger("voice.tts_engine")


class TTSProvider(str, Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    LOCAL = "local"  # Future: pyttsx3 / Coqui TTS for offline


class TTSEngine:
    """
    Text-to-Speech engine that routes to the appropriate provider
    based on the selected voice profile.
    """

    def __init__(self) -> None:
        self._openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._output_dir = Path("./audio_cache")
        self._output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("TTS Engine initialized")

    async def synthesize(
        self,
        text: str,
        voice_id: str = DEFAULT_VOICE_ID,
        output_path: Optional[Path] = None,
        speed: float = 1.0,
    ) -> bytes:
        """
        Convert text to speech audio bytes.

        Args:
            text: The text to speak.
            voice_id: Nova AI voice ID (maps to provider voice).
            output_path: Optional path to save the audio file.
            speed: Speech rate multiplier (0.25–4.0).

        Returns:
            Raw audio bytes (MP3 format).
        """
        voice_profile = get_voice_by_id(voice_id) or get_voice_by_id(DEFAULT_VOICE_ID)
        assert voice_profile is not None

        provider = self._select_provider(voice_profile)
        logger.debug(
            "TTS synthesis started",
            voice=voice_profile.name,
            provider=provider.value,
            text_len=len(text),
        )

        if provider == TTSProvider.OPENAI:
            audio_bytes = await self._synthesize_openai(text, voice_profile, speed)
        elif provider == TTSProvider.ELEVENLABS:
            audio_bytes = await self._synthesize_elevenlabs(text, voice_profile)
        else:
            audio_bytes = await self._synthesize_openai(text, voice_profile, speed)

        if output_path:
            output_path.write_bytes(audio_bytes)
            logger.debug("TTS audio saved", path=str(output_path))

        return audio_bytes

    def _select_provider(self, voice: VoiceProfile) -> TTSProvider:
        """Select TTS provider based on voice profile and available API keys."""
        if voice.elevenlabs_voice_id and settings.ELEVENLABS_API_KEY:
            return TTSProvider.ELEVENLABS
        return TTSProvider.OPENAI

    async def _synthesize_openai(
        self, text: str, voice: VoiceProfile, speed: float
    ) -> bytes:
        """Generate speech using OpenAI TTS API."""
        response = await self._openai.audio.speech.create(
            model="tts-1-hd",
            voice=voice.openai_voice,  # type: ignore[arg-type]
            input=text,
            response_format="mp3",
            speed=max(0.25, min(4.0, speed)),
        )
        return response.content

    async def _synthesize_elevenlabs(self, text: str, voice: VoiceProfile) -> bytes:
        """Generate speech using ElevenLabs API."""
        try:
            import httpx
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice.elevenlabs_voice_id}"
            headers = {
                "xi-api-key": settings.ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            }
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.75, "similarity_boost": 0.85},
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                return resp.content
        except Exception as exc:
            logger.warning("ElevenLabs TTS failed, falling back to OpenAI", error=str(exc))
            return await self._synthesize_openai(text, voice, speed=1.0)

    async def get_sample_audio(self, voice_id: str) -> bytes:
        """Generate a voice sample for the settings page preview."""
        voice = get_voice_by_id(voice_id)
        if not voice:
            raise ValueError(f"Unknown voice ID: {voice_id}")
        return await self.synthesize(
            text=voice.sample_text,
            voice_id=voice_id,
        )
