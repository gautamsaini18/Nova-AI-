"""Nova AI — Workflow Automation Engine

Allows users to create custom voice shortcuts,
automated workflows, and scheduled tasks.
"""

from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from backend.core.logging_config import NovaLogger

logger = NovaLogger("automation.engine")


@dataclass
class AutomationRule:
    id: str
    name: str
    trigger_phrase: str  # voice command that triggers this automation
    actions: list[dict]  # list of action definitions
    is_active: bool = True
    created_at: str = ""
    run_count: int = 0


@dataclass
class VoiceShortcut:
    id: str
    phrase: str
    response: str
    category: str = "custom"


class AutomationEngine:
    """
    Executes multi-step automation workflows in response to voice commands.
    Supports conditional logic, delays, and chained actions.
    """

    def __init__(self) -> None:
        self._rules: dict[str, AutomationRule] = {}
        self._shortcuts: dict[str, VoiceShortcut] = {}
        self._action_handlers: dict[str, Callable] = {}
        logger.info("AutomationEngine initialized")

    def register_action_handler(self, action_type: str, handler: Callable) -> None:
        """Register a handler for a specific action type."""
        self._action_handlers[action_type] = handler
        logger.debug("Action handler registered", action_type=action_type)

    def add_rule(self, rule: AutomationRule) -> str:
        """Add a new automation rule."""
        if not rule.id:
            rule.id = str(uuid.uuid4())
        if not rule.created_at:
            rule.created_at = datetime.now(timezone.utc).isoformat()
        self._rules[rule.id] = rule
        logger.info("Automation rule added", name=rule.name, trigger=rule.trigger_phrase)
        return rule.id

    def remove_rule(self, rule_id: str) -> bool:
        """Remove an automation rule."""
        return self._rules.pop(rule_id, None) is not None

    def add_shortcut(self, shortcut: VoiceShortcut) -> str:
        """Add a voice shortcut (quick phrase -> response)."""
        if not shortcut.id:
            shortcut.id = str(uuid.uuid4())
        self._shortcuts[shortcut.phrase.lower()] = shortcut
        logger.info("Voice shortcut added", phrase=shortcut.phrase)
        return shortcut.id

    def find_matching_rule(self, transcript: str) -> Optional[AutomationRule]:
        """Find a rule whose trigger phrase matches the transcript."""
        lower = transcript.lower()
        for rule in self._rules.values():
            if not rule.is_active:
                continue
            if rule.trigger_phrase.lower() in lower:
                return rule
        return None

    def find_shortcut(self, transcript: str) -> Optional[VoiceShortcut]:
        """Find a voice shortcut matching the transcript."""
        return self._shortcuts.get(transcript.lower().strip())

    async def execute_rule(self, rule: AutomationRule) -> list[Any]:
        """Execute all actions in an automation rule sequentially."""
        results = []
        for action in rule.actions:
            action_type = action.get("type")
            handler = self._action_handlers.get(action_type)
            if handler:
                try:
                    result = await handler(action.get("params", {}))
                    results.append({"action": action_type, "success": True, "result": result})
                except Exception as exc:
                    results.append({"action": action_type, "success": False, "error": str(exc)})
            else:
                results.append({"action": action_type, "success": False, "error": f"No handler for {action_type}"})

            # Support delays between actions
            delay = action.get("delay_seconds", 0)
            if delay > 0:
                await asyncio.sleep(delay)

        rule.run_count += 1
        logger.info("Automation rule executed", name=rule.name, actions=len(rule.actions))
        return results

    def list_rules(self) -> list[AutomationRule]:
        return list(self._rules.values())

    def list_shortcuts(self) -> list[VoiceShortcut]:
        return list(self._shortcuts.values())
