"""Statistics builder for Canonical Feature Collections.

Purpose:
    Aggregate pure structural counts and categories distribution metrics
    conforming strictly to Refinement 4.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.feature_engineering.models import Feature, FeatureStatistics


class FeatureStatisticsBuilder:
    """Builder assembling non-business structural metrics for canonical collections."""

    @classmethod
    def build(
        cls,
        features: Sequence[Feature],
        duplicate_count: int,
        error_count: int,
        warning_count: int,
    ) -> FeatureStatistics:
        """Calculate counts and compile FeatureStatistics.

        Args:
            features: Sequence of consolidated Feature objects.
            duplicate_count: resolved duplicate counts.
            error_count: validation errors count.
            warning_count: validation warnings count.

        Returns:
            The compiled FeatureStatistics model.
        """
        category_counts: dict[str, int] = {}
        for f in features:
            cat_name = f.category.value
            category_counts[cat_name] = category_counts.get(cat_name, 0) + 1

        return FeatureStatistics(
            total_feature_count=len(features),
            duplicate_count=duplicate_count,
            validation_error_count=error_count,
            warning_count=warning_count,
            category_counts=category_counts,
        )
