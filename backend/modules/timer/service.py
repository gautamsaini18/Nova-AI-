"""Nova AI — Timer & Stopwatch Service"""

from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import AsyncIterator, Callable


class TimerStatus(str, Enum):
    RUNNING = "running"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"


@dataclass
class Timer:
    id: str
    label: str
    duration_seconds: float
    remaining_seconds: float
    status: TimerStatus = TimerStatus.RUNNING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: datetime | None = None
    _task: asyncio.Task | None = None
    _paused_remaining: float | None = None

    @property
    def progress(self) -> float:
        if self.duration_seconds == 0:
            return 0.0
        return 1.0 - (self.remaining_seconds / self.duration_seconds)


@dataclass
class Stopwatch:
    id: str
    label: str
    elapsed_seconds: float = 0.0
    status: TimerStatus = TimerStatus.RUNNING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _start_time: float = field(default_factory=time.time)
    _task: asyncio.Task | None = None

    @property
    def current_elapsed(self) -> float:
        if self.status == TimerStatus.RUNNING:
            return self.elapsed_seconds + (time.time() - self._start_time)
        return self.elapsed_seconds


class TimerService:
    """Manages countdown timers and stopwatches."""

    def __init__(self):
        self._timers: dict[str, Timer] = {}
        self._stopwatches: dict[str, Stopwatch] = {}
        self._on_finish: Callable[[Timer], None] | None = None

    def on_timer_finish(self, callback: Callable[[Timer], None]) -> None:
        self._on_finish = callback

    # ── Timers ──────────────────────────────────────────────────────────────

    def create_timer(self, seconds: float, label: str = "Timer") -> Timer:
        tid = str(uuid.uuid4())[:8]
        timer = Timer(
            id=tid,
            label=label,
            duration_seconds=seconds,
            remaining_seconds=seconds,
        )
        self._timers[tid] = timer
        timer._task = asyncio.create_task(self._run_timer(timer))
        return timer

    async def _run_timer(self, timer: Timer) -> None:
        try:
            while timer.remaining_seconds > 0:
                if timer.status == TimerStatus.PAUSED:
                    await asyncio.sleep(0.1)
                    continue
                if timer.status == TimerStatus.CANCELLED:
                    return
                await asyncio.sleep(0.1)
                timer.remaining_seconds = max(0, timer.remaining_seconds - 0.1)

            timer.status = TimerStatus.FINISHED
            timer.finished_at = datetime.now(timezone.utc)
            if self._on_finish:
                self._on_finish(timer)
        except asyncio.CancelledError:
            pass

    def pause_timer(self, timer_id: str) -> Timer:
        timer = self._get_timer(timer_id)
        if timer.status != TimerStatus.RUNNING:
            raise ValueError(f"Timer {timer_id} is not running")
        timer.status = TimerStatus.PAUSED
        return timer

    def resume_timer(self, timer_id: str) -> Timer:
        timer = self._get_timer(timer_id)
        if timer.status != TimerStatus.PAUSED:
            raise ValueError(f"Timer {timer_id} is not paused")
        timer.status = TimerStatus.RUNNING
        if timer._task and timer._task.done():
            timer._task = asyncio.create_task(self._run_timer(timer))
        return timer

    def cancel_timer(self, timer_id: str) -> Timer:
        timer = self._get_timer(timer_id)
        timer.status = TimerStatus.CANCELLED
        if timer._task and not timer._task.done():
            timer._task.cancel()
        return timer

    def get_timer(self, timer_id: str) -> Timer | None:
        return self._timers.get(timer_id)

    def list_timers(self, status: TimerStatus | None = None) -> list[Timer]:
        timers = list(self._timers.values())
        if status:
            timers = [t for t in timers if t.status == status]
        return sorted(timers, key=lambda t: t.created_at, reverse=True)

    async def wait_for_timer(self, timer_id: str) -> Timer:
        timer = self._get_timer(timer_id)
        if timer._task:
            await timer._task
        return timer

    # ── Stopwatches ─────────────────────────────────────────────────────────

    def create_stopwatch(self, label: str = "Stopwatch") -> Stopwatch:
        sid = str(uuid.uuid4())[:8]
        sw = Stopwatch(id=sid, label=label)
        self._stopwatches[sid] = sw
        sw._task = asyncio.create_task(self._run_stopwatch(sw))
        return sw

    async def _run_stopwatch(self, sw: Stopwatch) -> None:
        try:
            while sw.status == TimerStatus.RUNNING:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass

    def pause_stopwatch(self, stopwatch_id: str) -> Stopwatch:
        sw = self._get_stopwatch(stopwatch_id)
        if sw.status != TimerStatus.RUNNING:
            raise ValueError(f"Stopwatch {stopwatch_id} is not running")
        sw.elapsed_seconds = sw.current_elapsed
        sw.status = TimerStatus.PAUSED
        if sw._task and not sw._task.done():
            sw._task.cancel()
        return sw

    def resume_stopwatch(self, stopwatch_id: str) -> Stopwatch:
        sw = self._get_stopwatch(stopwatch_id)
        if sw.status != TimerStatus.PAUSED:
            raise ValueError(f"Stopwatch {stopwatch_id} is not paused")
        sw._start_time = time.time()
        sw.status = TimerStatus.RUNNING
        sw._task = asyncio.create_task(self._run_stopwatch(sw))
        return sw

    def stop_stopwatch(self, stopwatch_id: str) -> Stopwatch:
        sw = self._get_stopwatch(stopwatch_id)
        sw.elapsed_seconds = sw.current_elapsed
        sw.status = TimerStatus.FINISHED
        if sw._task and not sw._task.done():
            sw._task.cancel()
        return sw

    def get_stopwatch(self, stopwatch_id: str) -> Stopwatch | None:
        return self._stopwatches.get(stopwatch_id)

    def list_stopwatches(self, status: TimerStatus | None = None) -> list[Stopwatch]:
        sws = list(self._stopwatches.values())
        if status:
            sws = [s for s in sws if s.status == status]
        return sorted(sws, key=lambda s: s.created_at, reverse=True)

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _get_timer(self, timer_id: str) -> Timer:
        timer = self._timers.get(timer_id)
        if not timer:
            raise KeyError(f"Timer '{timer_id}' not found")
        return timer

    def _get_stopwatch(self, stopwatch_id: str) -> Stopwatch:
        sw = self._stopwatches.get(stopwatch_id)
        if not sw:
            raise KeyError(f"Stopwatch '{stopwatch_id}' not found")
        return sw

    @staticmethod
    def format_seconds(seconds: float) -> str:
        total = int(seconds)
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        if h > 0:
            return f"{h}h {m}m {s}s"
        if m > 0:
            return f"{m}m {s}s"
        return f"{s}.{int((seconds % 1) * 10)}s"

    def cleanup_finished(self) -> int:
        """Remove finished/cancelled timers and stopwatches."""
        count = 0
        for tid in list(self._timers.keys()):
            t = self._timers[tid]
            if t.status in (TimerStatus.FINISHED, TimerStatus.CANCELLED) and t is not None:
                del self._timers[tid]
                count += 1
        for sid in list(self._stopwatches.keys()):
            s = self._stopwatches[sid]
            if s.status == TimerStatus.FINISHED:
                del self._stopwatches[sid]
                count += 1
        return count
