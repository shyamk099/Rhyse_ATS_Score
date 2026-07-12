"""Thread-safe cache for the active rule registry.

Purpose:
    Provide thread-safe storage and atomic retrieval of the current rule registry reference.
"""

from __future__ import annotations

import threading
from typing import Optional

from ats_engine.domain.rule_engine.registry import RuleRegistry


class RuleCache:
    """Thread-safe cache holding the active RuleRegistry reference."""

    def __init__(self) -> None:
        """Initialize the thread-safe rule cache."""
        self._lock = threading.Lock()
        self._registry: Optional[RuleRegistry] = None

    def get(self) -> Optional[RuleRegistry]:
        """Retrieve the active RuleRegistry snapshot thread-safely."""
        with self._lock:
            return self._registry

    def set(self, registry: RuleRegistry) -> None:
        """Atomically set the active RuleRegistry snapshot."""
        with self._lock:
            self._registry = registry

    def clear(self) -> None:
        """Clear the cached RuleRegistry reference."""
        with self._lock:
            self._registry = None
