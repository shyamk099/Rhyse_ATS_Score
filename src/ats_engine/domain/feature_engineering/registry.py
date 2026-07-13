"""Thread-safe Registry mapping feature types to stateless extractor classes.

Purpose:
    Provide mapping and dynamic registrations of string keys to
    FeatureExtractor class definitions.
"""

from __future__ import annotations

import threading
from typing import Type

from ats_engine.domain.feature_engineering.exceptions import RegistrationError
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor


class FeatureExtractorRegistry:
    """Registry maintaining mappings of extractor type keys to class references."""

    def __init__(self) -> None:
        """Initialize empty registry mappings and lock mechanism."""
        self._lock = threading.Lock()
        self._registry: dict[str, Type[FeatureExtractor]] = {}

    def register(self, extractor_type: str, extractor_cls: Type[FeatureExtractor]) -> None:
        """Register an extractor class type for a specific string identifier key.

        Args:
            extractor_type: Case-insensitive unique string identifier.
            extractor_cls: Extractor class conforming to FeatureExtractor interface.

        Raises:
            RegistrationError: If key is already registered.
        """
        key = extractor_type.strip().lower()
        if not key:
            raise RegistrationError("Extractor identifier key cannot be empty or whitespace.")

        with self._lock:
            if key in self._registry:
                raise RegistrationError(
                    f"Feature extractor type '{extractor_type}' is already registered."
                )
            self._registry[key] = extractor_cls

    def get(self, extractor_type: str) -> Type[FeatureExtractor] | None:
        """Retrieve class definition, or return None if unregistered."""
        key = extractor_type.strip().lower()
        with self._lock:
            return self._registry.get(key)

    def is_registered(self, extractor_type: str) -> bool:
        """Check if extractor type key exists in the registry."""
        key = extractor_type.strip().lower()
        with self._lock:
            return key in self._registry
