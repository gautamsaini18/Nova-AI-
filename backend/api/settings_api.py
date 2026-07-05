"""Nova AI — Settings API Router"""

from __future__ import annotations

from fastapi import APIRouter

from backend.core.logging_config import NovaLogger
from backend.models.schemas import UpdateSettingsRequest, UserSettings

logger = NovaLogger("api.settings")
router = APIRouter()

# In-memory store for demo (production: use DB)
_user_settings: dict[str, dict] = {}


def _default_settings() -> dict:
    return UserSettings().model_dump()


@router.get("/{user_id}")
async def get_settings(user_id: str):
    """Get user settings."""
    settings_data = _user_settings.get(user_id, _default_settings())
    return settings_data


@router.patch("/{user_id}")
async def update_settings(user_id: str, body: UpdateSettingsRequest):
    """Update user settings (partial update)."""
    current = _user_settings.get(user_id, _default_settings())
    updates = body.model_dump(exclude_none=True)
    current.update(updates)
    _user_settings[user_id] = current
    logger.info("Settings updated", user_id=user_id, fields=list(updates.keys()))
    return {"success": True, "settings": current}


@router.post("/{user_id}/reset")
async def reset_settings(user_id: str):
    """Reset user settings to defaults."""
    _user_settings[user_id] = _default_settings()
    return {"success": True, "settings": _user_settings[user_id]}
