"""Builder for CanonicalMatchCollection.

Purpose:
    Deteriministically sort and package matched results, statistics, and validation summary
    into the final immutable CanonicalMatchCollection DTO.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import (
    MatchResult,
    MatchStatistics,
    ValidationSummary,
    CanonicalMatchCollection,
)
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules


class CanonicalMatchCollectionBuilder:
    """Builder constructing frozen, immutable CanonicalMatchCollection objects."""

    @classmethod
    def build(
        cls,
        results: Sequence[MatchResult],
        statistics: MatchStatistics,
        validation_summary: ValidationSummary,
        rules: CanonicalMatchingRules,
    ) -> CanonicalMatchCollection:
        """Build the final sorted CanonicalMatchCollection.

        Args:
            results: Combined MatchResults.
            statistics: Compiled MatchStatistics DTO.
            validation_summary: Compiled ValidationSummary DTO.
            rules: Governing matching rules.

        Returns:
            An immutable CanonicalMatchCollection.
        """
        if rules.deterministic_ordering:
            sorted_results = sorted(
                results,
                key=lambda r: (
                    r.matcher_type or "",
                    r.resume_feature_id or "",
                    r.job_feature_id or "",
                ),
            )
        else:
            sorted_results = list(results)

        return CanonicalMatchCollection(
            results=tuple(sorted_results),
            statistics=statistics,
            validation_summary=validation_summary,
        )
