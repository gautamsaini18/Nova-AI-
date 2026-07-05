"""Nova AI — Device Control Module (Windows)

Controls OS-level features: volume, brightness, Wi-Fi,
Bluetooth, apps, power management, etc.
"""

from __future__ import annotations

import asyncio
import subprocess
from enum import Enum
from typing import Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("device_control.controller")


class PowerAction(Enum):
    SHUTDOWN = "shutdown"
    RESTART = "restart"
    SLEEP = "sleep"
    LOCK = "lock"
    LOGOFF = "logoff"


class DeviceController:
    """
    Controls Windows OS-level device features.
    Falls back gracefully on non-Windows platforms.
    """

    def __init__(self) -> None:
        self._is_windows = False
        import sys
        self._is_windows = sys.platform == "win32"
        logger.info("DeviceController initialized", platform=sys.platform)

    async def set_volume(self, level: int) -> bool:
        """Set system volume (0-100)."""
        if not self._is_windows:
            logger.warning("Volume control not supported on this platform")
            return False
        try:
            level = max(0, min(100, level))
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            logger.info("Volume set", level=level)
            return True
        except Exception as exc:
            logger.warning("Failed to set volume", error=str(exc))
            return False

    async def get_volume(self) -> Optional[int]:
        """Get current system volume (0-100)."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            scalar = volume.GetMasterVolumeLevelScalar()
            return int(scalar * 100)
        except Exception:
            return None

    async def set_brightness(self, level: int) -> bool:
        """Set display brightness (0-100)."""
        if not self._is_windows:
            return False
        try:
            level = max(0, min(100, level))
            import subprocess
            subprocess.run(
                ["powershell", "-c", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"],
                capture_output=True, timeout=5,
            )
            logger.info("Brightness set", level=level)
            return True
        except Exception as exc:
            logger.warning("Failed to set brightness", error=str(exc))
            return False

    async def launch_app(self, app_name: str) -> bool:
        """Launch an application by name."""
        try:
            if self._is_windows:
                subprocess.Popen(["start", app_name], shell=True)
            else:
                subprocess.Popen(["open", app_name])
            logger.info("App launched", app=app_name)
            return True
        except Exception as exc:
            logger.warning("Failed to launch app", app=app_name, error=str(exc))
            return False

    async def close_app(self, app_name: str) -> bool:
        """Close an application by name."""
        try:
            if self._is_windows:
                subprocess.run(["taskkill", "/F", "/IM", app_name], capture_output=True, timeout=5)
            else:
                subprocess.run(["pkill", "-f", app_name], capture_output=True, timeout=5)
            logger.info("App closed", app=app_name)
            return True
        except Exception as exc:
            logger.warning("Failed to close app", app=app_name, error=str(exc))
            return False

    async def open_website(self, url: str) -> bool:
        """Open a URL in the default browser."""
        try:
            import webbrowser
            webbrowser.open(url)
            logger.info("Website opened", url=url)
            return True
        except Exception as exc:
            logger.warning("Failed to open website", error=str(exc))
            return False

    async def power_action(self, action: PowerAction) -> bool:
        """Perform a system power action."""
        try:
            if not self._is_windows:
                return False
            commands = {
                PowerAction.SHUTDOWN: "shutdown /s /t 5",
                PowerAction.RESTART: "shutdown /r /t 5",
                PowerAction.SLEEP: "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
                PowerAction.LOCK: "rundll32.exe user32.dll,LockWorkStation",
                PowerAction.LOGOFF: "shutdown /l",
            }
            cmd = commands.get(action)
            if cmd:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
                logger.info("Power action executed", action=action.value)
                return True
            return False
        except Exception as exc:
            logger.warning("Power action failed", action=action.value, error=str(exc))
            return False

    async def get_battery_status(self) -> dict:
        """Get battery percentage and charging status."""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percentage": int(battery.percent),
                    "charging": battery.power_plugged or False,
                    "remaining_seconds": int(battery.secsleft) if battery.secsleft != -1 else None,
                }
            return {"percentage": None, "charging": None}
        except Exception:
            return {"percentage": None, "charging": None}

    async def get_storage_info(self) -> dict:
        """Get disk storage information."""
        try:
            import psutil
            usage = psutil.disk_usage("/")
            return {
                "total_gb": round(usage.total / (1024 ** 3), 1),
                "used_gb": round(usage.used / (1024 ** 3), 1),
                "free_gb": round(usage.free / (1024 ** 3), 1),
                "percent_used": usage.percent,
            }
        except Exception:
            return {}
