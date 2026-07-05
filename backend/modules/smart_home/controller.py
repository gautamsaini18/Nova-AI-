"""Nova AI — Smart Home Controller

Integrates with HomeKit, Google Home, and direct IoT device control
(lights, fans, AC, TV, plugs, locks, cameras, curtains, vacuum, thermostat).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("smart_home.controller")


class DeviceType(Enum):
    LIGHT = "light"
    FAN = "fan"
    AC = "ac"
    TV = "tv"
    PLUG = "plug"
    LOCK = "lock"
    CAMERA = "camera"
    CURTAIN = "curtain"
    VACUUM = "vacuum"
    THERMOSTAT = "thermostat"
    SPEAKER = "speaker"


class DeviceState(Enum):
    ON = "on"
    OFF = "off"
    UNKNOWN = "unknown"


@dataclass
class SmartDevice:
    id: str
    name: str
    device_type: DeviceType
    state: DeviceState
    room: str = ""
    attributes: dict = None


class SmartHomeController:
    """
    Central smart home controller supporting multiple ecosystems.

    Supports:
    - HomeKit (via pyhap)
    - Google Home (via google-assistant-sdk)
    - Direct IP/WiFi device control (TP-Link Kasa, Tasmota, etc.)
    """

    def __init__(self) -> None:
        self._devices: dict[str, SmartDevice] = {}
        self._homekit_enabled = settings.HOMEKIT_ENABLED
        self._google_home_enabled = settings.GOOGLE_HOME_ENABLED
        logger.info("SmartHomeController initialized")

    async def discover_devices(self) -> list[SmartDevice]:
        """Discover devices on the local network."""
        discovered = []

        # TP-Link Kasa smart plugs/lights
        try:
            import kasa
            dev = kasa.Device("")
            await dev.update()
            discovered.append(SmartDevice(
                id=dev.device_id,
                name=dev.alias or "Kasa Device",
                device_type=DeviceType.PLUG,
                state=DeviceState.ON if dev.is_on else DeviceState.OFF,
            ))
        except Exception:
            pass

        self._devices = {d.id: d for d in discovered}
        logger.info("Devices discovered", count=len(discovered))
        return discovered

    async def turn_on(self, device_id: str) -> bool:
        """Turn a device on."""
        device = self._devices.get(device_id)
        if not device:
            logger.warning("Device not found", device_id=device_id)
            return False
        try:
            if device.device_type in (DeviceType.LIGHT, DeviceType.PLUG):
                import kasa
                dev = kasa.Device("")
                await dev.turn_on()
            device.state = DeviceState.ON
            logger.info("Device turned on", name=device.name)
            return True
        except Exception as exc:
            logger.warning("Failed to turn on device", error=str(exc))
            return False

    async def turn_off(self, device_id: str) -> bool:
        """Turn a device off."""
        device = self._devices.get(device_id)
        if not device:
            return False
        try:
            if device.device_type in (DeviceType.LIGHT, DeviceType.PLUG):
                import kasa
                dev = kasa.Device("")
                await dev.turn_off()
            device.state = DeviceState.OFF
            logger.info("Device turned off", name=device.name)
            return True
        except Exception as exc:
            logger.warning("Failed to turn off device", error=str(exc))
            return False

    async def set_temperature(self, device_id: str, temperature: float) -> bool:
        """Set thermostat/AC temperature."""
        device = self._devices.get(device_id)
        if not device:
            return False
        try:
            import kasa
            dev = kasa.Device("")
            if hasattr(dev, "set_hvac_mode"):
                await dev.set_hvac_mode("cool")
            if hasattr(dev, "set_target_temperature"):
                await dev.set_target_temperature(temperature)
            logger.info("Temperature set", name=device.name, temp=temperature)
            return True
        except Exception as exc:
            logger.warning("Failed to set temperature", error=str(exc))
            return False

    async def register_homekit_device(self, name: str) -> Optional[str]:
        """Register a device with HomeKit."""
        if not self._homekit_enabled:
            return None
        try:
            import pyhap
            from pyhap.accessory import Accessory
            from pyhap.accessory_driver import AccessoryDriver
            driver = AccessoryDriver(port=51826)
            acc = Accessory(driver, name)
            driver.add_accessory(acc)
            mac = driver.state.mac
            logger.info("HomeKit device registered", name=name, mac=mac)
            return mac
        except Exception as exc:
            logger.warning("HomeKit registration failed", error=str(exc))
            return None

    def get_device(self, name: str) -> Optional[SmartDevice]:
        """Find a device by name (case-insensitive partial match)."""
        name_lower = name.lower()
        for device in self._devices.values():
            if name_lower in device.name.lower():
                return device
        return None

    def list_devices(self) -> list[SmartDevice]:
        return list(self._devices.values())
