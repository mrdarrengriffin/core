"""Support for Android IP Webcam Cameras."""

from __future__ import annotations

from homeassistant.components.mjpeg import MjpegCamera, filter_urllib3_logging
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
    HTTP_BASIC_AUTHENTICATION,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import AndroidIPCamConfigEntry, AndroidIPCamDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AndroidIPCamConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the IP Webcam camera from config entry."""
    filter_urllib3_logging()
    async_add_entities([IPWebcamCamera(config_entry.runtime_data)])


class IPWebcamCamera(MjpegCamera):
    """Representation of a IP Webcam camera."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AndroidIPCamDataUpdateCoordinator) -> None:
        """Initialize the camera."""
        super().__init__(
            mjpeg_url=coordinator.cam.mjpeg_url,
            still_image_url=coordinator.cam.image_url,
            authentication=HTTP_BASIC_AUTHENTICATION,
            username=coordinator.config_entry.data.get(CONF_USERNAME),
            password=coordinator.config_entry.data.get(CONF_PASSWORD, ""),
        )
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}-camera"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.data[CONF_HOST],
        )
