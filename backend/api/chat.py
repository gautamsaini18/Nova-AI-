"""Nova AI — Chat API Router"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from backend.core.config import settings
from backend.core.logging_config import NovaLogger
from backend.models.schemas import ChatRequest, ChatResponse
from backend.modules.ai_reasoning.agent import NovaAgent

logger = NovaLogger("api.chat")
router = APIRouter()

# Simple in-memory agent pool (production: use Redis / DB-backed sessions)
_agent_pool: dict[str, NovaAgent] = {}


def _get_agent(user_id: str, voice_id: str = "nova") -> NovaAgent:
    if user_id not in _agent_pool:
        _agent_pool[user_id] = NovaAgent(user_id=user_id, voice_name=voice_id)
    return _agent_pool[user_id]


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(body: ChatRequest) -> ChatResponse:
    """Send a message to Nova AI and receive a response."""
    conversation_id = body.conversation_id or str(uuid.uuid4())
    agent = _get_agent(body.user_id, body.voice_id)

    if body.stream:
        # Return streaming response
        async def token_generator() -> AsyncIterator[str]:
            async for token in await agent.chat(body.message, stream=True):
                yield f"data: {token}\n\n"
        return StreamingResponse(token_generator(), media_type="text/event-stream")

    response_text = await agent.chat(body.message)
    return ChatResponse(
        message=response_text,
        conversation_id=conversation_id,
        voice_id=body.voice_id,
        timestamp=datetime.now(timezone.utc),
    )


@router.delete("/{user_id}/history")
async def clear_history(user_id: str):
    """Clear conversation history for a user."""
    agent = _agent_pool.get(user_id)
    if agent:
        agent.clear_history()
    return {"success": True, "message": "Conversation history cleared"}


@router.get("/{user_id}/history")
async def get_history(user_id: str):
    """Get conversation history for a user."""
    agent = _agent_pool.get(user_id)
    history = agent.get_history() if agent else []
    return {"history": history, "count": len(history)}
