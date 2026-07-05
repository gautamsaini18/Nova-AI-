"""Nova AI — Speech Processing Module

Handles Voice Activity Detection (VAD), noise reduction,
and audio preprocessing before STT.
"""

from __future__ import annotations

import io
from enum import Enum
from typing import Optional

import numpy as np

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("speech_processing.processor")


class ProcessingStage(Enum):
    RAW = "raw"
    DENOISED = "denoised"
    NORMALIZED = "normalized"
    READY = "ready"


class SpeechProcessor:
    """
    Processes raw audio for optimal STT accuracy.

    Features:
    - Voice Activity Detection (VAD)
    - Noise reduction via spectral gating
    - Audio normalization
    - Format conversion
    """

    def __init__(self) -> None:
        self._sample_rate = settings.AUDIO_SAMPLE_RATE
        self._noise_reduction_enabled = settings.NOISE_REDUCTION_ENABLED
        logger.info("SpeechProcessor initialized")

    def reduce_noise(self, audio_data: bytes) -> bytes:
        """Apply noise reduction to raw PCM audio."""
        if not self._noise_reduction_enabled:
            return audio_data
        try:
            import noisereduce as nr
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            if len(audio_np) < 256:
                return audio_data
            reduced = nr.reduce_noise(y=audio_np, sr=self._sample_rate, prop_decrease=0.8)
            return reduced.astype(np.int16).tobytes()
        except Exception as exc:
            logger.warning("Noise reduction failed, using raw audio", error=str(exc))
            return audio_data

    def normalize(self, audio_data: bytes, target_dbfs: float = -20.0) -> bytes:
        """Normalize audio to a target dBFS level."""
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        if len(audio_np) == 0:
            return audio_data
        rms = np.sqrt(np.mean(audio_np ** 2))
        if rms < 1e-6:
            return audio_data
        target_rms = 10 ** (target_dbfs / 20)
        gain = target_rms / rms
        gain = min(max(gain, 0.1), 10.0)
        normalized = (audio_np * gain).astype(np.int16)
        return normalized.tobytes()

    def convert_to_wav(self, audio_data: bytes, sample_rate: Optional[int] = None) -> bytes:
        """Convert raw PCM bytes to WAV format bytes."""
        import wave
        sr = sample_rate or self._sample_rate
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(audio_data)
        return buf.getvalue()

    def is_speech_present(self, audio_data: bytes, threshold: float = 0.02) -> bool:
        """Simple energy-based VAD."""
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        if len(audio_np) == 0:
            return False
        rms = np.sqrt(np.mean(audio_np ** 2))
        return rms > threshold

    def process(self, audio_data: bytes) -> bytes:
        """Full processing pipeline: denoise -> normalize -> return."""
        processed = self.reduce_noise(audio_data)
        processed = self.normalize(processed)
        return processed
