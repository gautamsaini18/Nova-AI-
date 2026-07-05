"""Tests for Timer/Stopwatch Service."""

import asyncio
import pytest
from backend.modules.timer.service import TimerService, TimerStatus


class TestTimerService:
    @pytest.fixture
    def service(self):
        return TimerService()

    @pytest.mark.asyncio
    async def test_create_timer(self, service):
        timer = service.create_timer(60, "Test Timer")
        assert timer.label == "Test Timer"
        assert timer.duration_seconds == 60
        assert timer.remaining_seconds == 60
        assert timer.status == TimerStatus.RUNNING
        assert timer.progress == 0.0

    @pytest.mark.asyncio
    async def test_get_timer(self, service):
        timer = service.create_timer(30)
        assert service.get_timer(timer.id) is timer
        assert service.get_timer("nonexistent") is None

    @pytest.mark.asyncio
    async def test_list_timers(self, service):
        t1 = service.create_timer(10, "A")
        t2 = service.create_timer(20, "B")
        timers = service.list_timers()
        assert len(timers) == 2

    @pytest.mark.asyncio
    async def test_pause_resume_timer(self, service):
        timer = service.create_timer(60)
        assert timer.status == TimerStatus.RUNNING

        service.pause_timer(timer.id)
        assert timer.status == TimerStatus.PAUSED

        service.resume_timer(timer.id)
        assert timer.status == TimerStatus.RUNNING

    @pytest.mark.asyncio
    async def test_pause_not_running(self, service):
        timer = service.create_timer(60)
        service.pause_timer(timer.id)
        with pytest.raises(ValueError):
            service.pause_timer(timer.id)

    @pytest.mark.asyncio
    async def test_cancel_timer(self, service):
        timer = service.create_timer(60)
        service.cancel_timer(timer.id)
        assert timer.status == TimerStatus.CANCELLED

    def test_get_nonexistent_timer(self, service):
        with pytest.raises(KeyError):
            service.pause_timer("nonexistent")

    @pytest.mark.asyncio
    async def test_timer_runs_down(self):
        service = TimerService()
        timer = service.create_timer(0.3, "Quick")
        assert timer.remaining_seconds > 0

    @pytest.mark.asyncio
    async def test_timer_finishes(self):
        service = TimerService()
        timer = service.create_timer(0.2, "Quick")
        await service.wait_for_timer(timer.id)
        assert timer.status == TimerStatus.FINISHED
        assert timer.remaining_seconds == 0
        assert timer.finished_at is not None

    # ── Stopwatch Tests ────────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_create_stopwatch(self, service):
        sw = service.create_stopwatch("Test SW")
        assert sw.label == "Test SW"
        assert sw.status == TimerStatus.RUNNING
        assert sw.current_elapsed >= 0

    @pytest.mark.asyncio
    async def test_get_stopwatch(self, service):
        sw = service.create_stopwatch()
        assert service.get_stopwatch(sw.id) is sw
        assert service.get_stopwatch("nonexistent") is None

    @pytest.mark.asyncio
    async def test_pause_resume_stopwatch(self, service):
        sw = service.create_stopwatch()
        assert sw.status == TimerStatus.RUNNING

        service.pause_stopwatch(sw.id)
        assert sw.status == TimerStatus.PAUSED

        service.resume_stopwatch(sw.id)
        assert sw.status == TimerStatus.RUNNING

    @pytest.mark.asyncio
    async def test_stop_stopwatch(self, service):
        sw = service.create_stopwatch()
        service.stop_stopwatch(sw.id)
        assert sw.status == TimerStatus.FINISHED

    def test_format_seconds(self):
        assert TimerService.format_seconds(3661) == "1h 1m 1s"
        assert TimerService.format_seconds(125) == "2m 5s"
        assert TimerService.format_seconds(42) == "42.0s"
        assert TimerService.format_seconds(0) == "0.0s"

    @pytest.mark.asyncio
    async def test_cleanup_finished(self, service):
        service.create_timer(60)
        t2 = service.create_timer(60)
        service.cancel_timer(t2.id)
        count = service.cleanup_finished()
        assert count > 0
