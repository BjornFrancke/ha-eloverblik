"""Diagnostics support for Eloverblik Plus."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import EloverblikConfigEntry
from .const import CONF_REFRESH_TOKEN

TO_REDACT = {CONF_REFRESH_TOKEN}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: EloverblikConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    del hass

    runtime_data = entry.runtime_data
    client = runtime_data.client
    coordinator = runtime_data.coordinator

    return {
        "entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "unique_id": entry.unique_id,
            "data": async_redact_data(dict(entry.data), TO_REDACT),
            "options": async_redact_data(dict(entry.options), TO_REDACT),
        },
        "client": {
            "metering_point": client.metering_point,
            "local_time_zone": str(getattr(client, "_local_time_zone", None)),
            "has_cached_access_token": (
                getattr(client, "_access_token", None) is not None
            ),
            "access_token_expires_at": (
                getattr(client, "_access_token_expires_at", None).isoformat()
                if getattr(client, "_access_token_expires_at", None) is not None
                else None
            ),
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "data": coordinator.data,
        },
    }
