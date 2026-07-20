"""RecommendationOrchestrationBuilder definition.

Purpose:
    Group prioritized recommendations by section, category, and priority tier.
"""

from __future__ import annotations

from typing import Sequence, Mapping
from collections import defaultdict
from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class RecommendationOrchestrationBuilder:
    """Builder grouping prioritized recommendations into read-only Mapping structures."""

    @staticmethod
    def build_section_groups(
        recommendations: Sequence[Recommendation],
    ) -> Mapping[str, tuple[Recommendation, ...]]:
        """Group recommendations by section, preserving original sorted ordering."""
        groups: dict[str, list[Recommendation]] = defaultdict(list)
        for rec in recommendations:
            groups[rec.section].append(rec)
        return {k: tuple(v) for k, v in groups.items()}

    @staticmethod
    def build_category_groups(
        recommendations: Sequence[Recommendation],
    ) -> Mapping[str, tuple[Recommendation, ...]]:
        """Group recommendations by category, preserving original sorted ordering."""
        groups: dict[str, list[Recommendation]] = defaultdict(list)
        for rec in recommendations:
            groups[rec.category].append(rec)
        return {k: tuple(v) for k, v in groups.items()}

    @staticmethod
    def build_priority_groups(
        recommendations: Sequence[Recommendation],
        rules: PrioritizationRules,
    ) -> Mapping[str, tuple[Recommendation, ...]]:
        """Group recommendations by priority tier, preserving original sorted ordering."""
        groups: dict[str, list[Recommendation]] = {
            "High": [],
            "Medium": [],
            "Low": [],
        }
        for rec in recommendations:
            if rules.is_high(rec.priority):
                groups["High"].append(rec)
            elif rules.is_medium(rec.priority):
                groups["Medium"].append(rec)
            else:
                groups["Low"].append(rec)
        # Filter empty groups to keep mapping clean or keep them empty.
        # Let's keep empty groups so the structure is always complete and predictable.
        return {k: tuple(v) for k, v in groups.items()}
