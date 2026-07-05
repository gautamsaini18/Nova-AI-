"""Nova AI — Calendar & Scheduling Service

Manages events, reminders, alarms, and Google Calendar integration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("calendar.service")


@dataclass
class CalendarEvent:
    id: str
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    is_all_day: bool = False


@dataclass
class Reminder:
    id: str
    title: str
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    is_completed: bool = False
    is_recurring: bool = False


class CalendarService:
    """
    Calendar management with Google Calendar integration
    and local reminder/alarm scheduling.
    """

    def __init__(self) -> None:
        self._google_api_key = settings.GOOGLE_API_KEY
        logger.info("CalendarService initialized")

    def create_event(self, event: CalendarEvent) -> str:
        """Create a local calendar event (returns event ID)."""
        import uuid
        event.id = str(uuid.uuid4())
        logger.info("Calendar event created", title=event.title, event_id=event.id)
        return event.id

    async def get_upcoming_events(self, days: int = 7) -> list[CalendarEvent]:
        """Get upcoming events from Google Calendar."""
        if not self._google_api_key:
            logger.debug("Google API key not configured, returning empty")
            return []
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            creds = None
            service = build("calendar", "v3", credentials=creds, developerKey=self._google_api_key)
            now = datetime.utcnow().isoformat() + "Z"
            end = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"
            events_result = service.events().list(
                calendarId="primary", timeMin=now, timeMax=end,
                maxResults=20, singleEvents=True, orderBy="startTime",
            ).execute()
            events = []
            for e in events_result.get("items", []):
                start = e["start"].get("dateTime", e["start"].get("date"))
                end_t = e["end"].get("dateTime", e["end"].get("date"))
                events.append(CalendarEvent(
                    id=e["id"],
                    title=e["summary"],
                    description=e.get("description"),
                    start_time=datetime.fromisoformat(start) if start else None,
                    end_time=datetime.fromisoformat(end_t) if end_t else None,
                    location=e.get("location"),
                ))
            return events
        except Exception as exc:
            logger.warning("Failed to fetch calendar events", error=str(exc))
            return []

    async def schedule_reminder(self, reminder: Reminder) -> str:
        """Schedule a reminder (store and return ID)."""
        import uuid
        reminder.id = str(uuid.uuid4())
        logger.info("Reminder scheduled", title=reminder.title, at=str(reminder.scheduled_at))
        return reminder.id

    def format_event_response(self, events: list[CalendarEvent]) -> str:
        """Format events into a natural language response."""
        if not events:
            return "You have no upcoming events."
        lines = [f"You have {len(events)} upcoming event(s):"]
        for e in events:
            time_str = e.start_time.strftime("%A, %I:%M %p") if e.start_time else "All day"
            lines.append(f"• {e.title} — {time_str}")
        return "\n".join(lines)
