"""Nova AI — Music Player & Streaming Control

Integrates with Spotify, YouTube Music, and local file playback.
"""

from __future__ import annotations

import asyncio
import subprocess
from enum import Enum
from typing import Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("music.player")


class MusicSource(Enum):
    SPOTIFY = "spotify"
    YOUTUBE_MUSIC = "youtube_music"
    LOCAL = "local"
    APPLE_MUSIC = "apple_music"


class MusicPlayer:
    """
    Controls music playback across multiple sources.
    Uses Spotify Web API, yt-dlp for YouTube Music, and local playback.
    """

    def __init__(self) -> None:
        self._current_source: Optional[MusicSource] = None
        self._is_playing = False
        self._current_track: Optional[str] = None
        logger.info("MusicPlayer initialized")

    async def play_spotify(self, query: str, device_id: Optional[str] = None) -> bool:
        """Play a track/playlist on Spotify."""
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyOAuth
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id="", client_secret="",
                redirect_uri="http://localhost:8888/callback",
                scope="user-modify-playback-state user-read-playback-state",
            ))
            results = sp.search(q=query, type="track", limit=1)
            if results["tracks"]["items"]:
                track_uri = results["tracks"]["items"][0]["uri"]
                if device_id:
                    sp.start_playback(device_id=device_id, uris=[track_uri])
                else:
                    sp.start_playback(uris=[track_uri])
                self._is_playing = True
                self._current_source = MusicSource.SPOTIFY
                self._current_track = results["tracks"]["items"][0]["name"]
                logger.info("Spotify playback started", track=self._current_track)
                return True
            return False
        except Exception as exc:
            logger.warning("Spotify playback failed", error=str(exc))
            return False

    async def play_youtube_music(self, query: str) -> bool:
        """Play audio from YouTube Music using yt-dlp."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp", "-f", "bestaudio", "--get-url", f"ytsearch:{query}",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            url = stdout.decode().strip().split("\n")[0] if stdout else None
            if url:
                subprocess.Popen(["ffplay", "-nodisp", "-autoexit", url],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._is_playing = True
                self._current_source = MusicSource.YOUTUBE_MUSIC
                logger.info("YouTube Music playback started", query=query)
                return True
            return False
        except Exception as exc:
            logger.warning("YouTube Music playback failed", error=str(exc))
            return False

    async def play_local(self, file_path: str) -> bool:
        """Play a local audio file."""
        try:
            subprocess.Popen(["ffplay", "-nodisp", "-autoexit", file_path],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._is_playing = True
            self._current_source = MusicSource.LOCAL
            logger.info("Local playback started", path=file_path)
            return True
        except Exception as exc:
            logger.warning("Local playback failed", error=str(exc))
            return False

    async def stop(self) -> None:
        """Stop current playback."""
        try:
            subprocess.run(["pkill", "ffplay"], capture_output=True)
            self._is_playing = False
            logger.info("Playback stopped")
        except Exception:
            pass

    async def pause(self) -> None:
        """Pause current playback."""
        try:
            subprocess.run(["pkill", "-STOP", "ffplay"], capture_output=True)
            logger.info("Playback paused")
        except Exception:
            pass

    async def resume(self) -> None:
        """Resume paused playback."""
        try:
            subprocess.run(["pkill", "-CONT", "ffplay"], capture_output=True)
            logger.info("Playback resumed")
        except Exception:
            pass

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    @property
    def current_track(self) -> Optional[str]:
        return self._current_track
