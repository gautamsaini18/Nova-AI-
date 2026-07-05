"""
Nova AI — AI Reasoning Agent
Orchestrates conversations using OpenAI GPT with memory context injection.
"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator, List, Optional

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk

from backend.core.config import settings
from backend.core.logging_config import NovaLogger
from backend.modules.memory.memory_manager import MemoryManager

logger = NovaLogger("ai_reasoning.agent")


class NovaAgent:
    """
    Main AI reasoning agent for Nova AI.

    Responsibilities:
    - Maintain conversation context
    - Inject long-term memory
    - Route to specialized tools/skills
    - Stream or return responses
    """

    SYSTEM_PROMPT_TEMPLATE = """You are {assistant_name}, a next-generation AI voice assistant.

Personality:
- Warm, empathetic, and human-like in conversation
- Highly intelligent and knowledgeable across all domains
- Proactive — anticipate user needs
- Brief when appropriate, detailed when needed
- Never robotic or repetitive

Capabilities:
- Answer questions on any topic
- Help with productivity, scheduling, and reminders
- Control smart devices and apps
- Play music and entertainment
- Provide weather, news, and real-time info
- Code assistance, math, research
- Translations and language support
- Emotion-aware responses

Memory Context:
{memory_context}

User Profile:
- Name: {user_name}
- Language: {language}
- Voice: {voice_name}

Current Date/Time: {datetime}

Always respond naturally, as if speaking aloud. Keep responses concise for voice output (1-3 sentences unless more detail is required). If the user seems frustrated or upset, be extra empathetic."""

    def __init__(
        self,
        user_id: str,
        assistant_name: str = "Nova",
        user_name: str = "User",
        language: str = "English",
        voice_name: str = "Nova",
    ) -> None:
        self.user_id = user_id
        self.assistant_name = assistant_name
        self.user_name = user_name
        self.language = language
        self.voice_name = voice_name
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._memory: Optional[MemoryManager] = None
        self._conversation_history: List[dict] = []
        logger.info("NovaAgent initialized", user_id=user_id)

    async def _get_memory(self) -> MemoryManager:
        if self._memory is None:
            self._memory = await MemoryManager.create(self.user_id)
        return self._memory

    def _build_system_prompt(self, memory_context: str = "") -> str:
        from datetime import datetime
        return self.SYSTEM_PROMPT_TEMPLATE.format(
            assistant_name=self.assistant_name,
            memory_context=memory_context or "No specific memory context available.",
            user_name=self.user_name,
            language=self.language,
            voice_name=self.voice_name,
            datetime=datetime.now().strftime("%A, %B %d, %Y at %I:%M %p"),
        )

    def _truncate_history(self) -> List[dict]:
        """Return the most recent N messages to stay within context limits."""
        max_msgs = settings.MAX_CONTEXT_MESSAGES
        return self._conversation_history[-max_msgs:] if len(
            self._conversation_history
        ) > max_msgs else self._conversation_history

    async def chat(
        self,
        user_message: str,
        stream: bool = False,
    ) -> str:
        """
        Send a user message and get an AI response.

        Args:
            user_message: The user's input text.
            stream: If True, returns an async generator for streaming.

        Returns:
            The assistant's response as a string.
        """
        try:
            # Retrieve relevant memories
            memory_mgr = await self._get_memory()
            memories = await memory_mgr.search(user_message, limit=5)
            memory_context = "\n".join(
                f"- {m['content']}" for m in memories
            ) if memories else ""

            system_prompt = self._build_system_prompt(memory_context)

            # Add user message to history
            self._conversation_history.append({"role": "user", "content": user_message})

            messages = [
                {"role": "system", "content": system_prompt},
                *self._truncate_history(),
            ]

            if stream:
                return await self._stream_response(messages)

            response = await self._client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
            )
            assistant_message = response.choices[0].message.content or ""
            self._conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            # Auto-save important information to memory
            await memory_mgr.auto_extract_and_save(user_message, assistant_message)

            logger.debug("AI response generated", tokens=response.usage.total_tokens)
            return assistant_message

        except Exception as exc:
            logger.exception("Error generating AI response", error=str(exc))
            return (
                "I'm sorry, I encountered an issue processing your request. "
                "Please try again in a moment."
            )

    async def _stream_response(self, messages: List[dict]) -> AsyncIterator[str]:
        """Stream the AI response token by token."""
        full_response = ""
        async with self._client.chat.completions.stream(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
        ) as stream:
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    yield token

        self._conversation_history.append(
            {"role": "assistant", "content": full_response}
        )

    def clear_history(self) -> None:
        """Clear the in-memory conversation history."""
        self._conversation_history = []
        logger.info("Conversation history cleared", user_id=self.user_id)

    def get_history(self) -> List[dict]:
        """Return the full conversation history."""
        return list(self._conversation_history)
