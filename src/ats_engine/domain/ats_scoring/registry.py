"""ScoringRegistry definition.

Purpose:
    Provide thread-safe registry supporting registration, unregistration, priorities, and enabled configurations.
"""

from __future__ import annotations

import threading
from typing import Any

from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.exceptions import ScorerRegistrationError, UnsupportedScorerError


class ScoringRegistry:
    """Thread-safe, dependency-injectable registry for mapping scorer names to classes."""

    def __init__(self) -> None:
        """Initialize lock and entry storage map."""
        self._lock = threading.RLock()
        self._entries: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        scorer: type[AbstractScorer],
        priority: int = 100,
        enabled: bool = True,
    ) -> None:
        """Register an AbstractScorer subclass with a configuration metadata profile.

        Raises:
            ScorerRegistrationError: If class does not inherit from AbstractScorer.
        """
        with self._lock:
            if not isinstance(scorer, type) or not issubclass(scorer, AbstractScorer):
                raise ScorerRegistrationError(
                    f"Scorer '{scorer}' must be a class type inheriting from AbstractScorer."
                )
            self._entries[name] = {
                "scorer": scorer,
                "priority": priority,
                "enabled": enabled,
            }

    def unregister(self, name: str) -> None:
        """Remove a scorer registration by name."""
        with self._lock:
            if name not in self._entries:
                raise UnsupportedScorerError(f"Scorer '{name}' is not registered.")
            del self._entries[name]

    def get(self, name: str) -> type[AbstractScorer]:
        """Retrieve the registered class type.

        Raises:
            UnsupportedScorerError: If no class has been registered under this name.
        """
        with self._lock:
            if name not in self._entries:
                raise UnsupportedScorerError(f"Scorer '{name}' is not registered.")
            return self._entries[name]["scorer"]

    def list(self) -> list[str]:
        """List names of all registered scorers."""
        with self._lock:
            return list(self._entries.keys())

    def clear(self) -> None:
        """Clear all active registrations."""
        with self._lock:
            self._entries.clear()

    def get_metadata(self, name: str) -> dict[str, Any]:
        """Retrieve priority and enabled parameters for a registered scorer name."""
        with self._lock:
            if name not in self._entries:
                raise UnsupportedScorerError(f"Scorer '{name}' is not registered.")
            entry = self._entries[name]
            return {
                "priority": entry["priority"],
                "enabled": entry["enabled"],
            }
