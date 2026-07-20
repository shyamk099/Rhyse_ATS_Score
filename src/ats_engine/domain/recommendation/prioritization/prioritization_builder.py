"""PrioritizationBuilder definition.

Purpose:
    Copy, prioritize, and sort recommendations in deterministic ordering.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class PrioritizationBuilder:
    """Builder that copies, updates, and sorts recommendations based on PrioritizationRules."""

    @staticmethod
    def prioritize_and_sort(
        recommendations: Sequence[Recommendation],
        rules: PrioritizationRules,
    ) -> tuple[Recommendation, ...]:
        """Update each recommendation DTO with mapped attributes and sort them deterministically.

        Sorting Rules:
            1. Priority descending.
            2. Impact descending.
            3. Recommendation ID ascending (stable tie-breaker).
        """
        updated_recs: list[Recommendation] = []

        for rec in recommendations:
            profile = rules.resolve_profile(rec.section, rec.category)
            # copy and update fields
            updated = rec.model_copy(
                update={
                    "priority": profile.priority,
                    "impact": profile.impact,
                    "confidence": profile.confidence,
                }
            )
            updated_recs.append(updated)

        # Sort with deterministic tie-breaker: recommendation_id ASC
        updated_recs.sort(
            key=lambda r: (-r.priority, -r.impact, r.recommendation_id)
        )

        return tuple(updated_recs)
