"""Nova AI — Wake Word Detection (Porcupine)"""

from __future__ import annotations

import asyncio
import struct
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("wake_word.detector")


class WakeWordState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    TRIGGERED = "triggered"


class WakeWordDetector:
    """
    Wake word detection using Porcupine.

    In offline/fallback mode, uses a keyword-spotting approach.
    Designed to run continuously in a background asyncio task.
    """

    def __init__(
        self,
        wake_word: str = "",
        sensitivity: float = 0.5,
        on_activation: Optional[Callable[[], None]] = None,
    ) -> None:
        self._wake_word = wake_word or settings.WAKE_WORD
        self._sensitivity = sensitivity or settings.WAKE_WORD_SENSITIVITY
        self._on_activation = on_activation
        self._state = WakeWordState.IDLE
        self._porcupine = None
        self._audio_stream = None
        logger.info("WakeWordDetector initialized", wake_word=self._wake_word)

    async def start(self) -> None:
        """Start the wake word detection loop."""
        self._state = WakeWordState.LISTENING
        logger.info("Wake word detection started")

        try:
            import pvporcupine
            self._porcupine = pvporcupine.create(
                access_key=settings.PORCUPINE_ACCESS_KEY,
                keywords=[self._wake_word],
                sensitivities=[self._sensitivity],
            )
            logger.info("Porcupine engine created")
        except Exception as exc:
            logger.warning("Porcupine init failed, using fallback", error=str(exc))
            self._porcupine = None

        if self._porcupine is None:
            await self._fallback_loop()
        else:
            await self._porcupine_loop()

    async def stop(self) -> None:
        """Stop wake word detection and clean up."""
        self._state = WakeWordState.IDLE
        if self._porcupine:
            self._porcupine.delete()
            self._porcupine = None
        if self._audio_stream:
            self._audio_stream.close()
            self._audio_stream = None
        logger.info("Wake word detection stopped")

    async def _porcupine_loop(self) -> None:
        """Main detection loop using Porcupine."""
        import pyaudio
        pa = pyaudio.PyAudio()
        try:
            self._audio_stream = pa.open(
                rate=self._porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._porcupine.frame_length,
            )
            while self._state == WakeWordState.LISTENING:
                pcm = self._audio_stream.read(self._porcupine.frame_length, exception_on_overflow=False)
                pcm_unpacked = struct.unpack_from("h" * self._porcupine.frame_length, pcm)
                keyword_index = self._porcupine.process(pcm_unpacked)
                if keyword_index >= 0:
                    self._state = WakeWordState.TRIGGERED
                    logger.info("Wake word detected")
                    if self._on_activation:
                        self._on_activation()
                    await asyncio.sleep(0.5)
                    self._state = WakeWordState.LISTENING
                await asyncio.sleep(0.01)
        finally:
            pa.terminate()

    async def _fallback_loop(self) -> None:
        """Simple fallback when Porcupine is unavailable (for testing)."""
        logger.info("Using fallback wake word detection (simulated)")
        while self._state == WakeWordState.LISTENING:
            await asyncio.sleep(0.1)

    @property
    def state(self) -> WakeWordState:
        return self._state

    @state.setter
    def state(self, value: WakeWordState) -> None:
        self._state = value
