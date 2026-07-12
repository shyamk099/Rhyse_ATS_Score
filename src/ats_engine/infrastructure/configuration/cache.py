"""Thread-safe cache for immutable infrastructure settings.

Purpose:
    Avoid repeated source loading while retaining explicit cache ownership.

TODO:
    Keep cache keys limited to infrastructure source identity.

Future responsibilities:
    Support controlled configuration refresh by approved outer-layer wiring.

Handbook reference:
    Book 01 - System Architecture.
"""

from __future__ import annotations

import logging
from pathlib import Path
from threading import RLock

from ats_engine.infrastructure.configuration.models import ApplicationSettings, Environment

ConfigurationCacheKey = tuple[Environment, Path | None, Path | None, tuple[tuple[str, str], ...]]


class ConfigurationCache:
    """Own a lock-protected cache of immutable settings by source identity."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Initialize an empty cache with an optional structured-logging hook."""
        self._entries: dict[ConfigurationCacheKey, ApplicationSettings] = {}
        self._lock = RLock()
        self._logger = logger or logging.getLogger(__name__)

    def get(self, key: ConfigurationCacheKey) -> ApplicationSettings | None:
        """Return a cached immutable settings value for a validated cache key."""
        with self._lock:
            setting = self._entries.get(key)
        self._logger.debug("configuration_cache_lookup", extra={"cache_hit": setting is not None})
        return setting

    def set(self, key: ConfigurationCacheKey, settings: ApplicationSettings) -> None:
        """Store immutable settings under a validated infrastructure-source key."""
        with self._lock:
            self._entries[key] = settings
        self._logger.debug("configuration_cache_updated", extra={"environment": settings.environment.value})

    def clear(self) -> None:
        """Clear all cached settings through the cache owner's explicit API."""
        with self._lock:
            self._entries.clear()
        self._logger.debug("configuration_cache_cleared")
