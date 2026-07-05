"""
Nova AI — Memory Manager
Manages long-term memory using ChromaDB (vector similarity) + SQLite (structured).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("memory.manager")


class MemoryManager:
    """
    Handles long-term memory for Nova AI using ChromaDB.

    Features:
    - Store user preferences, facts, and notes
    - Semantic similarity search for context injection
    - Auto-extract facts from conversations
    - Forget specific memories (privacy mode)
    """

    def __init__(self, user_id: str, collection: Any) -> None:
        self.user_id = user_id
        self._collection = collection

    @classmethod
    async def create(cls, user_id: str) -> "MemoryManager":
        """Async factory to initialize ChromaDB and return a MemoryManager."""
        client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        collection_name = f"{settings.CHROMA_COLLECTION_NAME}_{user_id}"
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("MemoryManager initialized", user_id=user_id, collection=collection_name)
        return cls(user_id=user_id, collection=collection)

    async def remember(
        self,
        content: str,
        memory_type: str = "fact",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Store a new memory.

        Args:
            content: The memory content to store.
            memory_type: One of 'fact', 'preference', 'note', 'conversation'.
            metadata: Additional key-value pairs to store.

        Returns:
            The ID of the stored memory.
        """
        memory_id = str(uuid.uuid4())
        meta = {
            "user_id": self.user_id,
            "type": memory_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **(metadata or {}),
        }
        self._collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[memory_id],
        )
        logger.debug("Memory stored", memory_id=memory_id, type=memory_type)
        return memory_id

    async def search(
        self,
        query: str,
        limit: int = 5,
        memory_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search memories by semantic similarity.

        Args:
            query: The search query.
            limit: Maximum number of results.
            memory_type: Filter by memory type.

        Returns:
            List of matching memory dicts with content and metadata.
        """
        where_filter = {"user_id": self.user_id}
        if memory_type:
            where_filter["type"] = memory_type  # type: ignore[assignment]

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=min(limit, self._collection.count() or 1),
                where=where_filter,
            )
        except Exception as exc:
            logger.warning("Memory search failed", error=str(exc))
            return []

        memories = []
        if results["documents"]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                if dist <= (1 - settings.MEMORY_SIMILARITY_THRESHOLD):
                    memories.append({"content": doc, "metadata": meta, "similarity": 1 - dist})
        return memories

    async def forget(self, memory_id: str) -> bool:
        """Delete a specific memory by ID."""
        try:
            self._collection.delete(ids=[memory_id])
            logger.info("Memory deleted", memory_id=memory_id)
            return True
        except Exception as exc:
            logger.warning("Memory deletion failed", memory_id=memory_id, error=str(exc))
            return False

    async def forget_all(self) -> int:
        """Delete ALL memories for this user. Returns count deleted."""
        try:
            count = self._collection.count()
            # Delete all docs matching user_id
            results = self._collection.get(where={"user_id": self.user_id})
            if results["ids"]:
                self._collection.delete(ids=results["ids"])
            logger.warning("All memories deleted", user_id=self.user_id, count=count)
            return count
        except Exception as exc:
            logger.error("Failed to delete all memories", error=str(exc))
            return 0

    async def get_all(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return all memories for this user (paginated)."""
        try:
            results = self._collection.get(
                where={"user_id": self.user_id},
                limit=limit,
                include=["documents", "metadatas"],
            )
            return [
                {"id": id_, "content": doc, "metadata": meta}
                for id_, doc, meta in zip(
                    results["ids"], results["documents"], results["metadatas"]
                )
            ]
        except Exception as exc:
            logger.warning("Failed to retrieve memories", error=str(exc))
            return []

    async def auto_extract_and_save(
        self, user_message: str, assistant_response: str
    ) -> None:
        """
        Automatically extract important facts from a conversation turn
        and save them to memory. Called after each AI response.
        """
        # Simple heuristics — in production, use GPT to extract facts
        important_phrases = [
            "my name is", "i am", "i live in", "i work at", "i prefer",
            "i love", "i hate", "remember that", "don't forget", "my favorite",
            "i usually", "i always", "i never", "remind me", "my birthday",
        ]
        lower_msg = user_message.lower()
        for phrase in important_phrases:
            if phrase in lower_msg:
                await self.remember(
                    content=f"User said: {user_message}",
                    memory_type="preference",
                    metadata={"source": "auto_extract", "trigger": phrase},
                )
                logger.debug("Auto-extracted memory", trigger=phrase)
                break
