"""Nova AI — Timer/Stopwatch API Router"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.core.logging_config import NovaLogger
from backend.models.schemas import (
    StopwatchCreateRequest, StopwatchResponse,
    TimerCreateRequest, TimerResponse,
)
from backend.modules.timer.service import TimerService

logger = NovaLogger("api.timer")
router = APIRouter()

_timer_service = TimerService()


def _timer_to_response(t) -> TimerResponse:
    return TimerResponse(
        id=t.id,
        label=t.label,
        duration_seconds=t.duration_seconds,
        remaining_seconds=max(0, t.remaining_seconds),
        progress=round(t.progress, 4),
        status=t.status.value,
        created_at=t.created_at,
        finished_at=t.finished_at,
        formatted_remaining=TimerService.format_seconds(max(0, t.remaining_seconds)),
        formatted_duration=TimerService.format_seconds(t.duration_seconds),
    )


def _stopwatch_to_response(s) -> StopwatchResponse:
    return StopwatchResponse(
        id=s.id,
        label=s.label,
        elapsed_seconds=round(s.current_elapsed, 2),
        status=s.status.value,
        created_at=s.created_at,
        formatted_elapsed=TimerService.format_seconds(s.current_elapsed),
    )


@router.post("/timers", response_model=TimerResponse, status_code=201)
async def create_timer(body: TimerCreateRequest):
    """Create a countdown timer."""
    timer = _timer_service.create_timer(body.seconds, body.label)
    return _timer_to_response(timer)


@router.get("/timers", response_model=list[TimerResponse])
async def list_timers(status: str | None = None):
    """List all timers, optionally filtered by status."""
    from backend.modules.timer.service import TimerStatus
    status_filter = TimerStatus(status) if status else None
    return [_timer_to_response(t) for t in _timer_service.list_timers(status_filter)]


@router.get("/timers/{timer_id}", response_model=TimerResponse)
async def get_timer(timer_id: str):
    """Get a specific timer."""
    timer = _timer_service.get_timer(timer_id)
    if not timer:
        raise HTTPException(404, detail=f"Timer '{timer_id}' not found")
    return _timer_to_response(timer)


@router.post("/timers/{timer_id}/pause", response_model=TimerResponse)
async def pause_timer(timer_id: str):
    """Pause a running timer."""
    try:
        timer = _timer_service.pause_timer(timer_id)
        return _timer_to_response(timer)
    except (KeyError, ValueError) as e:
        raise HTTPException(400, detail=str(e))


@router.post("/timers/{timer_id}/resume", response_model=TimerResponse)
async def resume_timer(timer_id: str):
    """Resume a paused timer."""
    try:
        timer = _timer_service.resume_timer(timer_id)
        return _timer_to_response(timer)
    except (KeyError, ValueError) as e:
        raise HTTPException(400, detail=str(e))


@router.delete("/timers/{timer_id}", response_model=TimerResponse)
async def cancel_timer(timer_id: str):
    """Cancel a timer."""
    try:
        timer = _timer_service.cancel_timer(timer_id)
        return _timer_to_response(timer)
    except KeyError as e:
        raise HTTPException(404, detail=str(e))


@router.post("/stopwatches", response_model=StopwatchResponse, status_code=201)
async def create_stopwatch(body: StopwatchCreateRequest):
    """Create a stopwatch."""
    sw = _timer_service.create_stopwatch(body.label)
    return _stopwatch_to_response(sw)


@router.get("/stopwatches", response_model=list[StopwatchResponse])
async def list_stopwatches(status: str | None = None):
    """List all stopwatches."""
    from backend.modules.timer.service import TimerStatus
    status_filter = TimerStatus(status) if status else None
    return [_stopwatch_to_response(s) for s in _timer_service.list_stopwatches(status_filter)]


@router.get("/stopwatches/{stopwatch_id}", response_model=StopwatchResponse)
async def get_stopwatch(stopwatch_id: str):
    """Get a specific stopwatch."""
    sw = _timer_service.get_stopwatch(stopwatch_id)
    if not sw:
        raise HTTPException(404, detail=f"Stopwatch '{stopwatch_id}' not found")
    return _stopwatch_to_response(sw)


@router.post("/stopwatches/{stopwatch_id}/pause", response_model=StopwatchResponse)
async def pause_stopwatch(stopwatch_id: str):
    """Pause a running stopwatch."""
    try:
        sw = _timer_service.pause_stopwatch(stopwatch_id)
        return _stopwatch_to_response(sw)
    except (KeyError, ValueError) as e:
        raise HTTPException(400, detail=str(e))


@router.post("/stopwatches/{stopwatch_id}/resume", response_model=StopwatchResponse)
async def resume_stopwatch(stopwatch_id: str):
    """Resume a paused stopwatch."""
    try:
        sw = _timer_service.resume_stopwatch(stopwatch_id)
        return _stopwatch_to_response(sw)
    except (KeyError, ValueError) as e:
        raise HTTPException(400, detail=str(e))


@router.post("/stopwatches/{stopwatch_id}/stop", response_model=StopwatchResponse)
async def stop_stopwatch(stopwatch_id: str):
    """Stop a stopwatch."""
    try:
        sw = _timer_service.stop_stopwatch(stopwatch_id)
        return _stopwatch_to_response(sw)
    except KeyError as e:
        raise HTTPException(404, detail=str(e))
