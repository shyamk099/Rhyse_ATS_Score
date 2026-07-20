"""BasePostProcessor abstract base class.

Purpose:
    Define post-processing pipeline stages for RecommendationEngine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import RecommendationResult


class BasePostProcessor(ABC):
    """Abstract base class for post-processing recommendation results."""

    @abstractmethod
    def process(self, result: RecommendationResult) -> Any:
        """Process the RecommendationResult and return a processed DTO.

        Args:
            result: The raw RecommendationResult from providers.

        Returns:
            The processed result (e.g. PrioritizedRecommendationResult).
        """
        ...
