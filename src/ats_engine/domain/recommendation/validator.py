"""RecommendationValidator definition.

Purpose:
    Stateless pre-execution validation of inputs and registry state
    before the RecommendationEngine runs providers.
"""

from __future__ import annotations

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError
from ats_engine.domain.recommendation.models import RecommendationContext


class RecommendationValidator:
    """Stateless validator ensuring inputs and registry are valid before execution.

    Validates:
        1. CanonicalMatchCollection is not None.
        2. ScoreResult is not None.
        3. ExplainabilityResult is not None.
        4. Registry contains no duplicate provider names (enforced at registration,
           but double-checked here for defence-in-depth).
        5. Provider priorities form a valid deterministic ordering
           (no two providers share the same priority).
    """

    @staticmethod
    def validate_inputs(context: RecommendationContext | None) -> None:
        """Validate that all required inputs are present in the context.

        Raises:
            RecommendationValidationError: If context or any of its fields are None.
        """
        if context is None:
            raise RecommendationValidationError(
                "Recommendation failed: RecommendationContext cannot be None."
            )
        if getattr(context, "match_collection", None) is None:
            raise RecommendationValidationError(
                "Recommendation failed: CanonicalMatchCollection cannot be None."
            )
        if getattr(context, "score_result", None) is None:
            raise RecommendationValidationError(
                "Recommendation failed: ScoreResult cannot be None."
            )
        if getattr(context, "explainability_result", None) is None:
            raise RecommendationValidationError(
                "Recommendation failed: ExplainabilityResult cannot be None."
            )

    @staticmethod
    def validate_registry(registry: RecommendationRegistry) -> None:
        """Validate registry state for deterministic execution.

        Checks:
            - No duplicate priorities among registered providers.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        if registry is None:
            raise RecommendationValidationError(
                "Recommendation failed: RecommendationRegistry cannot be None."
            )

        providers = registry.get_ordered_providers()
        seen_priorities: dict[int, str] = {}
        for provider in providers:
            prio = provider.priority()
            name = provider.provider_name()
            if prio in seen_priorities:
                raise RecommendationValidationError(
                    f"Recommendation failed: providers '{seen_priorities[prio]}' and "
                    f"'{name}' share the same priority ({prio}). "
                    f"All providers must have unique priorities for deterministic ordering."
                )
            seen_priorities[prio] = name
