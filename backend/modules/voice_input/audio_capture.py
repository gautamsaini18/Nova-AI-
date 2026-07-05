"""Nova AI — Audio Capture Module

Captures microphone input, detects voice activity,
and streams audio chunks for STT processing.
"""

from __future__ import annotations

import asyncio
import queue
import struct
import threading
from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator, Callable, Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("voice_input.audio_capture")


class AudioState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"


@dataclass
class AudioChunk:
    data: bytes
    timestamp: float
    is_speech: bool = False


class AudioCapture:
    """
    Captures audio from the microphone in real-time.
    Uses a background thread to read from PyAudio and
    exposes an async iterator for consuming audio chunks.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        silence_threshold: float = 0.02,
    ) -> None:
        self.sample_rate = sample_rate or settings.AUDIO_SAMPLE_RATE
        self.channels = channels or settings.AUDIO_CHANNELS
        self.chunk_size = chunk_size or settings.AUDIO_CHUNK_SIZE
        self._silence_threshold = silence_threshold
        self._state = AudioState.IDLE
        self._audio_queue: queue.Queue[bytes] = queue.Queue()
        self._stream = None
        self._pa = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
        logger.info("AudioCapture initialized")

    async def start(self) -> None:
        """Start capturing audio."""
        import pyaudio
        self._state = AudioState.LISTENING
        self._running = True
        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._callback,
        )
        self._stream.start_stream()
        logger.info("Audio capture started")

    def _callback(self, in_data: bytes, frame_count: int, time_info: dict, status: int):
        """PyAudio stream callback — runs in background thread."""
        self._audio_queue.put(in_data)
        return (None, 0)

    async def stop(self) -> None:
        """Stop capturing audio."""
        self._running = False
        self._state = AudioState.IDLE
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        if self._pa:
            self._pa.terminate()
        logger.info("Audio capture stopped")

    async def stream(self) -> AsyncIterator[AudioChunk]:
        """Async iterator yielding audio chunks as they arrive."""
        import time
        while self._running or not self._audio_queue.empty():
            try:
                data = await asyncio.get_event_loop().run_in_executor(
                    None, self._audio_queue.get, True, 0.1
                )
                yield AudioChunk(
                    data=data,
                    timestamp=time.time(),
                    is_speech=not self._is_silence(data),
                )
            except queue.Empty:
                await asyncio.sleep(0.01)

    def _is_silence(self, data: bytes) -> bool:
        """Simple RMS-based silence detection."""
        if len(data) < 2:
            return True
        fmt = "<{}h".format(len(data) // 2)
        try:
            samples = struct.unpack(fmt, data)
            rms = sum(s * s for s in samples) / len(samples)
            return rms < self._silence_threshold
        except (struct.error, ZeroDivisionError):
            return True

    @property
    def state(self) -> AudioState:
        return self._state
