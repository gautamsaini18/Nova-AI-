"""Nova AI — Voice API Router"""

from __future__ import annotations

import asyncio
import io
from typing import AsyncIterator, List, Set

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import Response, StreamingResponse

from backend.core.logging_config import NovaLogger
from backend.models.schemas import STTResponse, VoiceProfile, VoiceSynthesisRequest
from backend.modules.voice.tts_engine import TTSEngine
from backend.modules.voice.voice_profiles import (
    VOICE_LIBRARY,
    get_all_categories,
    get_voice_by_id,
    voice_to_dict,
)

logger = NovaLogger("api.voice")
router = APIRouter()
_tts_engine = TTSEngine()

# ── Interrupt-Speaking Support ──────────────────────────────────────────────────
_interrupt_events: dict[str, asyncio.Event] = {}


async def _token_generator_with_interrupt(
    text: str,
    voice_id: str,
    speed: float,
    stream_id: str,
    chunk_size: int = 4096,
) -> AsyncIterator[bytes]:
    """Generate audio chunks with interrupt support."""
    event = asyncio.Event()
    _interrupt_events[stream_id] = event

    try:
        audio_bytes = await _tts_engine.synthesize(
            text=text, voice_id=voice_id, speed=speed,
        )
        for i in range(0, len(audio_bytes), chunk_size):
            if event.is_set():
                logger.info("Stream interrupted", stream_id=stream_id)
                break
            chunk = audio_bytes[i:i + chunk_size]
            yield chunk
            await asyncio.sleep(0)
    finally:
        _interrupt_events.pop(stream_id, None)


@router.get("/voices", response_model=List[VoiceProfile])
async def list_voices():
    """Return all available voice profiles."""
    return [voice_to_dict(v) for v in VOICE_LIBRARY]


@router.get("/voices/categories")
async def list_voices_by_category():
    """Return voices grouped by category."""
    categories = get_all_categories()
    return {
        cat: [voice_to_dict(v) for v in voices]
        for cat, voices in categories.items()
    }


@router.get("/voices/{voice_id}")
async def get_voice(voice_id: str):
    """Get a specific voice profile by ID."""
    voice = get_voice_by_id(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail=f"Voice '{voice_id}' not found")
    return voice_to_dict(voice)


@router.post("/synthesize")
async def synthesize_speech(body: VoiceSynthesisRequest):
    """Convert text to speech audio (MP3)."""
    audio_bytes = await _tts_engine.synthesize(
        text=body.text,
        voice_id=body.voice_id,
        speed=body.speed,
    )
    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )


@router.get("/sample/{voice_id}")
async def get_voice_sample(voice_id: str):
    """Get a sample audio preview for a specific voice."""
    voice = get_voice_by_id(voice_id)
    if not voice:
        raise HTTPException(status_code=404, detail=f"Voice '{voice_id}' not found")
    audio_bytes = await _tts_engine.get_sample_audio(voice_id)
    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": f"inline; filename={voice_id}_sample.mp3"},
    )


@router.post("/synthesize/stream")
async def synthesize_speech_stream(body: VoiceSynthesisRequest):
    """Stream TTS audio with interrupt support."""
    import uuid
    stream_id = str(uuid.uuid4())[:8]
    return StreamingResponse(
        _token_generator_with_interrupt(
            text=body.text,
            voice_id=body.voice_id,
            speed=body.speed,
            stream_id=stream_id,
        ),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "inline; filename=speech.mp3",
            "X-Stream-Id": stream_id,
        },
    )


@router.post("/stop/{stream_id}")
async def stop_synthesis(stream_id: str):
    """Interrupt an ongoing TTS stream."""
    event = _interrupt_events.get(stream_id)
    if not event:
        raise HTTPException(404, detail=f"No active stream '{stream_id}'")
    event.set()
    return {"success": True, "message": f"Stream '{stream_id}' interrupted"}


@router.post("/transcribe", response_model=STTResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = "en",
):
    """Transcribe uploaded audio file using Whisper."""
    from openai import AsyncOpenAI
    from backend.core.config import settings

    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    audio_data = await file.read()

    try:
        transcript = await client.audio.transcriptions.create(
            model="whisper-1",
            file=(file.filename or "audio.webm", io.BytesIO(audio_data), file.content_type),
            language=language if language != "auto" else None,
        )
        return STTResponse(
            text=transcript.text,
            language=language,
        )
    except Exception as exc:
        logger.exception("STT transcription failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Transcription failed")
