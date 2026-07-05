"""Nova AI — Plugin System

Dynamic plugin loading, management, and lifecycle.
Supports Python and JavaScript plugins via pluggy.
"""

from __future__ import annotations

import importlib
import inspect
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from backend.core.logging_config import NovaLogger

logger = NovaLogger("plugins.manager")


@dataclass
class PluginInfo:
    name: str
    version: str
    description: str
    author: str
    entry_point: str
    enabled: bool = True
    hooks: list[str] = field(default_factory=list)


class PluginManager:
    """
    Manages the lifecycle of plugins.

    Plugins are loaded from the `plugins/` directory.
    Each plugin can register hooks that the assistant calls at specific points.
    """

    def __init__(self, plugin_dir: str = "plugins") -> None:
        self._plugin_dir = Path(plugin_dir)
        self._plugin_dir.mkdir(parents=True, exist_ok=True)
        self._plugins: dict[str, PluginInfo] = {}
        self._loaded_modules: dict[str, Any] = {}
        self._hook_registry: dict[str, list[Callable]] = {}
        logger.info("PluginManager initialized", directory=str(self._plugin_dir))

    def discover_plugins(self) -> list[PluginInfo]:
        """Scan the plugin directory for available plugins."""
        discovered = []
        sys.path.insert(0, str(self._plugin_dir.parent))

        for item in self._plugin_dir.iterdir():
            if item.suffix == ".py" and not item.name.startswith("_"):
                plugin_name = item.stem
                try:
                    spec = importlib.util.spec_from_file_location(plugin_name, str(item))
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        info = PluginInfo(
                            name=getattr(mod, "__plugin_name__", plugin_name),
                            version=getattr(mod, "__version__", "1.0.0"),
                            description=getattr(mod, "__description__", ""),
                            author=getattr(mod, "__author__", "Unknown"),
                            entry_point=plugin_name,
                            hooks=[name for name in dir(mod) if name.startswith("on_")],
                        )
                        self._plugins[plugin_name] = info
                        self._loaded_modules[plugin_name] = mod
                        discovered.append(info)
                        logger.info("Plugin discovered", name=info.name, version=info.version)
                except Exception as exc:
                    logger.warning("Failed to load plugin", plugin=plugin_name, error=str(exc))

        sys.path.pop(0)
        return discovered

    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin (re-register its hooks)."""
        if name not in self._plugins:
            return False
        self._plugins[name].enabled = True
        self._register_hooks(name)
        logger.info("Plugin enabled", name=name)
        return True

    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin (unregister its hooks)."""
        if name not in self._plugins:
            return False
        self._plugins[name].enabled = False
        mod = self._loaded_modules.get(name)
        if mod:
            for hook_name in dir(mod):
                if hook_name.startswith("on_"):
                    self._hook_registry.pop(hook_name, None)
        logger.info("Plugin disabled", name=name)
        return True

    def _register_hooks(self, plugin_name: str) -> None:
        """Register all hooks from a plugin."""
        mod = self._loaded_modules.get(plugin_name)
        if not mod:
            return
        for hook_name in dir(mod):
            if hook_name.startswith("on_"):
                hook_fn = getattr(mod, hook_name)
                if callable(hook_fn):
                    self._hook_registry.setdefault(hook_name, []).append(hook_fn)

    def trigger_hook(self, hook_name: str, *args: Any, **kwargs: Any) -> list[Any]:
        """Trigger a specific hook across all enabled plugins."""
        results = []
        for fn in self._hook_registry.get(hook_name, []):
            try:
                result = fn(*args, **kwargs)
                results.append(result)
            except Exception as exc:
                logger.warning("Hook execution failed", hook=hook_name, error=str(exc))
        return results

    def list_plugins(self) -> list[PluginInfo]:
        return list(self._plugins.values())
