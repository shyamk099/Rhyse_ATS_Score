"""Abstract interface definition for stateless Feature Extractors.

Purpose:
    Expose a clean abstract base class mapping CanonicalEntityCollections
    to generic, immutable Feature sequences.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection
from ats_engine.domain.feature_engineering.models import Feature, FeatureExtractionContext


class FeatureExtractor(ABC):
    """Abstract base class establishing the stateless FeatureExtractor interface."""

    @abstractmethod
    def extract(
        self,
        canonical_entities: CanonicalEntityCollection,
        context: FeatureExtractionContext,
    ) -> Sequence[Feature]:
        """Scan canonical entities and construct features.

        Args:
            canonical_entities: The CanonicalEntityCollection containing all extracted data.
            context: Context containing rules, correlation id, and execution config.

        Returns:
            A sequence of stateless, immutable Feature DTOs.
        """
        pass
