"""Registry mapping extractor type identifiers to extractor class implementations.

Purpose:
    Provide decoupling between pipeline resolving and concrete extractor lookups.
"""

from __future__ import annotations

from typing import Type

from ats_engine.domain.entity_extraction.exceptions import ExtractorRegistrationError
from ats_engine.domain.entity_extraction.extractor import EntityExtractor


class EntityExtractorRegistry:
    """Registry maintaining unique mappings of extractor type keys to class definitions."""

    def __init__(self) -> None:
        """Initialize empty registry mappings."""
        self._registry: dict[str, Type[EntityExtractor]] = {}

    def register(self, extractor_type: str, extractor_cls: Type[EntityExtractor]) -> None:
        """Register an extractor class definition for an type identifier key.

        Args:
            extractor_type: Unique string identifier (e.g. 'skills').
            extractor_cls: Reference to class conforming to EntityExtractor.

        Raises:
            ExtractorRegistrationError: If key is already registered.
        """
        key = extractor_type.lower()
        if key in self._registry:
            raise ExtractorRegistrationError(
                f"Extractor type '{extractor_type}' is already registered in this scope."
            )
        self._registry[key] = extractor_cls

    def get(self, extractor_type: str) -> Type[EntityExtractor] | None:
        """Retrieve class definition, or return None if unregistered."""
        return self._registry.get(extractor_type.lower())
