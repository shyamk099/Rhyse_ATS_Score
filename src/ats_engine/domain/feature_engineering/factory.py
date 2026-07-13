"""Factory instantiating stateless extractor classes.

Purpose:
    Expose a service to dynamically retrieve/instantiate FeatureExtractor
    implementations from registry definitions.
"""

from __future__ import annotations

from ats_engine.domain.feature_engineering.exceptions import UnknownExtractorError
from ats_engine.domain.feature_engineering.extractor import FeatureExtractor
from ats_engine.domain.feature_engineering.registry import FeatureExtractorRegistry


class FeatureExtractorFactory:
    """Factory resolving registry keys and returning FeatureExtractor instances."""

    def __init__(self, registry: FeatureExtractorRegistry) -> None:
        """Initialize factory with registry mapping context."""
        self._registry = registry

    def get_extractor(self, extractor_type: str) -> FeatureExtractor:
        """Instantiate a stateless extractor instance based on its string key.

        Args:
            extractor_type: String key registered.

        Returns:
            An instantiated FeatureExtractor object.

        Raises:
            UnknownExtractorError: If type key has no registered class.
        """
        extractor_cls = self._registry.get(extractor_type)
        if not extractor_cls:
            raise UnknownExtractorError(
                f"No feature extractor registered for type: '{extractor_type}'"
            )
        return extractor_cls()
