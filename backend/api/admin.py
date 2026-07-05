"""Nova AI — Admin API Router"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import func, select

from backend.core.config import settings
from backend.core.logging_config import NovaLogger
from backend.database.session import async_session_factory as AsyncSessionLocal
from backend.models.schemas import PluginInfo, SystemStats, UserListItem

logger = NovaLogger("api.admin")
router = APIRouter()

_start_time = time.time()


def _get_db_path() -> str:
    url = settings.database_url
    if url.startswith("sqlite"):
        path = url.replace("sqlite+aiosqlite:///", "")
        return os.path.abspath(path) if not path.startswith("/") else path
    return ""


@router.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """Return system-wide statistics."""
    from backend.database.models import Conversation, Memory, Message, Reminder, User

    db_path = _get_db_path()
    db_size = os.path.getsize(db_path) if db_path and os.path.exists(db_path) else 0

    stats = SystemStats(
        uptime_seconds=round(time.time() - _start_time, 2),
        version=settings.APP_VERSION,
        database_size_bytes=db_size,
    )

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(func.count(User.id)))
            stats.total_users = result.scalar() or 0

            result = await session.execute(select(func.count(Conversation.id)))
            stats.total_conversations = result.scalar() or 0

            result = await session.execute(select(func.count(Message.id)))
            stats.total_messages = result.scalar() or 0

            result = await session.execute(select(func.count(Memory.id)))
            stats.total_memories = result.scalar() or 0

            result = await session.execute(select(func.count(Reminder.id)))
            stats.total_reminders = result.scalar() or 0
    except Exception as e:
        logger.warning("Could not fetch DB stats", error=str(e))

    return stats


@router.get("/users", response_model=list[UserListItem])
async def list_users(skip: int = 0, limit: int = 50):
    """List all registered users."""
    from backend.database.models import Conversation, User

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
            )
            users = result.scalars().all()

            items = []
            for u in users:
                conv_count = await session.execute(
                    select(func.count(Conversation.id)).where(Conversation.user_id == u.id)
                )
                items.append(UserListItem(
                    id=u.id,
                    name=u.name,
                    email=u.email,
                    plan=u.plan,
                    is_active=u.is_active,
                    created_at=u.created_at,
                    last_active=u.last_active,
                    conversation_count=conv_count.scalar() or 0,
                ))
            return items
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.get("/plugins", response_model=list[PluginInfo])
async def list_plugins():
    """List available plugins and their status."""
    try:
        from backend.modules.plugins.manager import PluginManager
        pm = PluginManager()
        return [
            PluginInfo(
                name=name,
                version=getattr(plugin, "__version__", "0.1.0"),
                enabled=pm.is_enabled(name),
                description=getattr(plugin, "__doc__", "") or "",
            )
            for name, plugin in pm.list_plugins().items()
        ]
    except Exception as e:
        logger.warning("Could not load plugins", error=str(e))
        return []


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(user_id: str):
    """Deactivate a user account."""
    from backend.database.models import User
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(404, detail=f"User '{user_id}' not found")
            user.is_active = False
            await session.commit()
            return {"success": True, "message": f"User '{user_id}' deactivated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.post("/users/{user_id}/activate")
async def activate_user(user_id: str):
    """Activate a user account."""
    from backend.database.models import User
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(404, detail=f"User '{user_id}' not found")
            user.is_active = True
            await session.commit()
            return {"success": True, "message": f"User '{user_id}' activated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))
