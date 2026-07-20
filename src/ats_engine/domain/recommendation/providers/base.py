"""BaseRecommendationProvider abstract base class.

Purpose:
    Define the contract that all recommendation providers must implement.
    Providers are registered with the RecommendationRegistry and executed
    in deterministic priority order by the RecommendationEngine.

    Concrete providers (skill_provider, experience_provider, etc.) will be
    added in Milestones 7.2+.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from enum import Enum

if TYPE_CHECKING:
    from ats_engine.domain.recommendation.models import Recommendation, RecommendationContext


class RecommendationAction(str, Enum):
    """Provider-agnostic actions representing evaluation outcomes."""

    NO_ACTION = "NO_ACTION"
    MISSING = "MISSING"
    PARTIAL = "PARTIAL"
    LEVEL_GAP = "LEVEL_GAP"
    DURATION_GAP = "DURATION_GAP"
    RELATED_GAP = "RELATED_GAP"
    EXPIRED = "EXPIRED"


class BaseRecommendationValidator:
    """Base validator providing shared logic for checking recommendation bounds."""

    @staticmethod
    def validate_recommendation_bounds(
        recommendations: list[Recommendation] | tuple[Recommendation, ...],
        expected_section: str,
        allowed_categories: tuple[str, ...],
    ) -> None:
        """Validate recommendation fields, sections, and category constraints.

        Args:
            recommendations: The sequence of recommendations to validate.
            expected_section: The expected section name.
            allowed_categories: A tuple of permitted categories.

        Raises:
            RecommendationValidationError: If any bounds check fails.
        """
        from ats_engine.domain.recommendation.exceptions import RecommendationValidationError

        seen_ids: set[str] = set()
        seen_titles: set[str] = set()

        for rec in recommendations:
            if rec.section != expected_section:
                raise RecommendationValidationError(
                    f"Accidental cross-emission detected: section must be '{expected_section}', got '{rec.section}'"
                )
            if not rec.title or rec.title.strip() == "":
                raise RecommendationValidationError(f"{expected_section.capitalize()} recommendation title cannot be empty.")
            if not rec.description or rec.description.strip() == "":
                raise RecommendationValidationError(f"{expected_section.capitalize()} recommendation description cannot be empty.")
            if rec.category not in allowed_categories:
                raise RecommendationValidationError(
                    f"Invalid category '{rec.category}' for {expected_section} recommendation."
                )

            if rec.recommendation_id in seen_ids:
                raise RecommendationValidationError(
                    f"Duplicate recommendation ID detected: {rec.recommendation_id}"
                )
            if rec.title in seen_titles:
                raise RecommendationValidationError(
                    f"Duplicate recommendation title detected: {rec.title}"
                )

            seen_ids.add(rec.recommendation_id)
            seen_titles.add(rec.title)


class BaseRecommendationProvider(ABC):
    """Abstract base class for deterministic recommendation providers.

    Every provider must:
        1. Have a unique provider_name().
        2. Have a deterministic priority() (lower = runs first).
        3. Implement validate() to check pre-conditions.
        4. Implement generate() to produce a tuple of Recommendation DTOs.

    Providers MUST NOT:
        - Use AI, LLMs, or embeddings.
        - Access external services.
        - Modify input DTOs.
    """

    @abstractmethod
    def provider_name(self) -> str:
        """Return the unique name of this provider (e.g. 'SKILL', 'EXPERIENCE')."""
        ...

    @abstractmethod
    def priority(self) -> int:
        """Return the execution priority (lower value = earlier execution).

        Deterministic ordering is enforced by the registry.
        """
        ...

    @abstractmethod
    def validate(self, context: "RecommendationContext") -> None:
        """Validate that this provider can execute given the context.

        Raises:
            RecommendationProviderError: If validation fails.
        """
        ...

    @abstractmethod
    def generate(self, context: "RecommendationContext") -> tuple["Recommendation", ...]:
        """Generate a tuple of deterministic Recommendation DTOs.

        Returns:
            An immutable tuple of Recommendation objects.
        """
        ...

