"""SkillRecommendationRules definition.

Purpose:
    Define deterministic rules governing skill recommendation categories.
"""

from __future__ import annotations


class SkillRecommendationRules:
    """Deterministic rules governing when a skill matching classification should be recommended.

    Categories:
        - SKILL_MISSING (Recommended = True)
        - SKILL_PARTIAL_MATCH (Recommended = True)
        - SKILL_EQUIVALENT (Recommended = False)
        - EXACT (Recommended = False)
    """

    def should_recommend(self, classification: str) -> bool:
        """Determine if a recommendation should be generated for a classification type.

        Args:
            classification: The classification string (e.g. 'SKILL_MISSING', 'SKILL_PARTIAL_MATCH').

        Returns:
            True if the classification warrants a recommendation, False otherwise.
        """
        # Missing or partial match warrants a recommendation
        if classification in ("SKILL_MISSING", "SKILL_PARTIAL_MATCH"):
            return True
        return False
