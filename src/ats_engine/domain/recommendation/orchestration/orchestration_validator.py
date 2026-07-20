"""RecommendationOrchestrationValidator definition.

Purpose:
    Provide strict validation of orchestrated recommendation results.
"""

from __future__ import annotations

from typing import Sequence, Mapping
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError


class RecommendationOrchestrationValidator:
    """Validator verifying grouping counts, uniqueness, reference identity, and sorting sequence."""

    @staticmethod
    def validate(
        recommendations: Sequence[Recommendation],
        by_section: Mapping[str, tuple[Recommendation, ...]],
        by_category: Mapping[str, tuple[Recommendation, ...]],
        by_priority: Mapping[str, tuple[Recommendation, ...]],
    ) -> None:
        """Validate orchestrated recommendation mappings.

        Checks:
            - Uniqueness: no duplicate recommendation IDs.
            - Uniqueness: no duplicate object reference identities.
            - Conservation: total recommendations match grouped recommendation totals.
            - Alignment: every recommendation in groups matches those in the main list.
            - Preserved sorting: grouped lists preserve original sorting order.

        Raises:
            RecommendationValidationError: If validation fails.
        """
        main_ids = {r.recommendation_id for r in recommendations}
        main_refs = {id(r) for r in recommendations}

        if len(main_ids) != len(recommendations):
            raise RecommendationValidationError("Duplicate recommendation ID detected in main list.")
        if len(main_refs) != len(recommendations):
            raise RecommendationValidationError("Duplicate object reference detected in main list.")

        # Conservation check: Section
        sec_total = sum(len(v) for v in by_section.values())
        if sec_total != len(recommendations):
            raise RecommendationValidationError(
                f"Conservation mismatch: total is {len(recommendations)}, but by_section sum is {sec_total}"
            )

        # Conservation check: Category
        cat_total = sum(len(v) for v in by_category.values())
        if cat_total != len(recommendations):
            raise RecommendationValidationError(
                f"Conservation mismatch: total is {len(recommendations)}, but by_category sum is {cat_total}"
            )

        # Conservation check: Priority
        pri_total = sum(len(v) for v in by_priority.values())
        if pri_total != len(recommendations):
            raise RecommendationValidationError(
                f"Conservation mismatch: total is {len(recommendations)}, but by_priority sum is {pri_total}"
            )

        # Helper to verify sorting and references
        for mapping_name, groups in [("section", by_section), ("category", by_category), ("priority", by_priority)]:
            for group_name, group_list in groups.items():
                prev_idx = -1
                for rec in group_list:
                    if id(rec) not in main_refs:
                        raise RecommendationValidationError(
                            f"Orphaned recommendation {rec.recommendation_id} in {mapping_name} group {group_name}"
                        )
                    # Find its index in the main list to verify stable sorting
                    current_idx = next(i for i, r in enumerate(recommendations) if id(r) == id(rec))
                    if current_idx < prev_idx:
                        raise RecommendationValidationError(
                            f"Sorting sequence violated in {mapping_name} group {group_name}"
                        )
                    prev_idx = current_idx
