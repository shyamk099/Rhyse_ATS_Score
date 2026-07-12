"""Factory resolving and instantiating stateless extractor classes.

Purpose:
    Expose a clean interface to retrieve extractor instances based on registry definitions.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.exceptions import UnknownExtractorError
from ats_engine.domain.entity_extraction.extractor import EntityExtractor
from ats_engine.domain.entity_extraction.registry import EntityExtractorRegistry


class EntityExtractorFactory:
    """Factory determining extractor classes and returning stateless extractor instances."""

    def __init__(self, registry: EntityExtractorRegistry) -> None:
        """Initialize factory with registry dependencies."""
        self._registry = registry

    def get_extractor(self, extractor_type: str) -> EntityExtractor:
        """Instantiate a stateless extractor for a type identifier.

        Args:
            extractor_type: String code of extractor.

        Returns:
            An instantiated, stateless EntityExtractor object.

        Raises:
            UnknownExtractorError: If the type is not registered.
        """
        extractor_cls = self._registry.get(extractor_type)
        if not extractor_cls:
            raise UnknownExtractorError(f"No extractor registered for type: '{extractor_type}'")
        return extractor_cls()
