"""Nova AI — Voice Authentication & Security

Voice-based authentication, speaker identification,
privacy mode, and permission management.
"""

from __future__ import annotations

import io
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

from backend.core.logging_config import NovaLogger

logger = NovaLogger("security.voice_auth")


@dataclass
class AuthResult:
    authenticated: bool
    user_id: Optional[str] = None
    confidence: float = 0.0
    error: Optional[str] = None


class VoiceAuthenticator:
    """
    Voice-based authentication using speaker embedding.

    Uses speechbrain or a simple MFCC + GMM approach
    to identify and verify speakers.
    """

    def __init__(self) -> None:
        self._model_dir = Path("./voice_models")
        self._model_dir.mkdir(parents=True, exist_ok=True)
        self._speaker_profiles: dict[str, np.ndarray] = {}
        self._load_profiles()
        logger.info("VoiceAuthenticator initialized")

    def _load_profiles(self) -> None:
        """Load saved speaker profiles from disk."""
        profile_file = self._model_dir / "speaker_profiles.pkl"
        if profile_file.exists():
            try:
                with open(profile_file, "rb") as f:
                    self._speaker_profiles = pickle.load(f)
                logger.info("Speaker profiles loaded", count=len(self._speaker_profiles))
            except Exception as exc:
                logger.warning("Failed to load speaker profiles", error=str(exc))

    def _save_profiles(self) -> None:
        """Save speaker profiles to disk."""
        profile_file = self._model_dir / "speaker_profiles.pkl"
        try:
            with open(profile_file, "wb") as f:
                pickle.dump(self._speaker_profiles, f)
            logger.debug("Speaker profiles saved")
        except Exception as exc:
            logger.warning("Failed to save speaker profiles", error=str(exc))

    def _extract_embedding(self, audio_data: bytes) -> Optional[np.ndarray]:
        """Extract a speaker embedding from audio data."""
        try:
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            if len(audio_np) < 4000:
                return None
            mfccs = self._compute_mfcc(audio_np)
            return np.mean(mfccs, axis=0)
        except Exception as exc:
            logger.warning("Embedding extraction failed", error=str(exc))
            return None

    def _compute_mfcc(self, audio: np.ndarray, n_mfcc: int = 13) -> np.ndarray:
        """Compute MFCC features from audio signal."""
        try:
            import librosa
            mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=n_mfcc)
            return mfccs.T
        except ImportError:
            logger.warning("librosa not available, using simplified features")
            frame_size = 400
            hop_size = 160
            frames = [audio[i:i + frame_size] for i in range(0, len(audio) - frame_size, hop_size)]
            features = []
            for frame in frames:
                if len(frame) > 0:
                    fft = np.abs(np.fft.rfft(frame))
                    features.append(fft[:n_mfcc])
            return np.array(features) if features else np.zeros((1, n_mfcc))

    async def enroll_user(self, user_id: str, audio_data: bytes) -> bool:
        """Enroll a new user by creating a voice profile."""
        embedding = self._extract_embedding(audio_data)
        if embedding is None:
            logger.warning("Failed to extract embedding for enrollment", user_id=user_id)
            return False
        self._speaker_profiles[user_id] = embedding
        self._save_profiles()
        logger.info("User enrolled", user_id=user_id)
        return True

    async def authenticate(self, audio_data: bytes, threshold: float = 0.75) -> AuthResult:
        """Authenticate a user by their voice against enrolled profiles."""
        embedding = self._extract_embedding(audio_data)
        if embedding is None:
            return AuthResult(authenticated=False, error="Could not extract voice features")

        if not self._speaker_profiles:
            return AuthResult(authenticated=False, error="No users enrolled")

        best_score = -1.0
        best_user = None
        for user_id, profile in self._speaker_profiles.items():
            similarity = self._cosine_similarity(embedding, profile)
            if similarity > best_score:
                best_score = similarity
                best_user = user_id

        if best_score >= threshold and best_user:
            return AuthResult(authenticated=True, user_id=best_user, confidence=best_score)
        return AuthResult(authenticated=False, confidence=best_score)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        a_flat = a.flatten()
        b_flat = b.flatten()
        min_len = min(len(a_flat), len(b_flat))
        a_flat, b_flat = a_flat[:min_len], b_flat[:min_len]
        dot = np.dot(a_flat, b_flat)
        norm = (np.linalg.norm(a_flat) * np.linalg.norm(b_flat)) or 1
        return float(dot / norm)

    def remove_user(self, user_id: str) -> bool:
        """Remove a user's voice profile."""
        if user_id in self._speaker_profiles:
            del self._speaker_profiles[user_id]
            self._save_profiles()
            logger.info("User voice profile removed", user_id=user_id)
            return True
        return False

    def list_enrolled_users(self) -> list[str]:
        return list(self._speaker_profiles.keys())
