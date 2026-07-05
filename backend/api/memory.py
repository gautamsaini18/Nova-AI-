"""Nova AI — Memory API Router"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.core.logging_config import NovaLogger
from backend.models.schemas import MemoryEntry, RememberRequest, SearchMemoryRequest
from backend.modules.memory.memory_manager import MemoryManager

logger = NovaLogger("api.memory")
router = APIRouter()


async def _get_memory_manager(user_id: str) -> MemoryManager:
    return await MemoryManager.create(user_id)


@router.post("/{user_id}/remember")
async def remember(user_id: str, body: RememberRequest):
    """Store a new memory for a user."""
    mgr = await _get_memory_manager(user_id)
    memory_id = await mgr.remember(
        content=body.content,
        memory_type=body.memory_type,
        metadata=body.metadata,
    )
    return {"success": True, "memory_id": memory_id}


@router.post("/{user_id}/search")
async def search_memory(user_id: str, body: SearchMemoryRequest):
    """Search memories by semantic similarity."""
    mgr = await _get_memory_manager(user_id)
    results = await mgr.search(
        query=body.query,
        limit=body.limit,
        memory_type=body.memory_type,
    )
    return {"results": results, "count": len(results)}


@router.get("/{user_id}/all")
async def get_all_memories(user_id: str, limit: int = 50):
    """Get all memories for a user."""
    mgr = await _get_memory_manager(user_id)
    memories = await mgr.get_all(limit=limit)
    return {"memories": memories, "count": len(memories)}


@router.delete("/{user_id}/forget/{memory_id}")
async def forget_memory(user_id: str, memory_id: str):
    """Delete a specific memory."""
    mgr = await _get_memory_manager(user_id)
    deleted = await mgr.forget(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"success": True}


@router.delete("/{user_id}/forget-all")
async def forget_all_memories(user_id: str):
    """Delete all memories for a user (privacy reset)."""
    mgr = await _get_memory_manager(user_id)
    count = await mgr.forget_all()
    return {"success": True, "deleted_count": count}
