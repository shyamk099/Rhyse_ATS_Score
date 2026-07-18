"""Duplicate match resolver for MatchResults.

Purpose:
    Filter and resolve duplicate MatchResult entries based on configured policies.
    Supports KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, and KEEP_ALL.
    Performs no merges or synthesis.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.matching.models import MatchResult
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules


class DuplicateMatchResolver:
    """Resolver for deduplicating MatchResults based on resume/job feature ID pairs."""

    @classmethod
    def resolve(
        cls,
        results: Sequence[MatchResult],
        rules: CanonicalMatchingRules,
    ) -> tuple[Sequence[MatchResult], int]:
        """Resolve duplicate MatchResults.

        Args:
            results: Sequence of MatchResults to process.
            rules: Configuration rules payload.

        Returns:
            A tuple containing:
                - The deduplicated sequence of MatchResults.
                - The count of duplicate results removed/skipped.
        """
        policy = rules.duplicate_policy
        if policy == "KEEP_ALL" or not results:
            return results, 0

        seen: dict[tuple[str, str], list[MatchResult]] = {}
        for r in results:
            key = (r.resume_feature_id, r.job_feature_id)
            seen.setdefault(key, []).append(r)

        resolved_results: list[MatchResult] = []
        duplicate_count = 0

        for key, matches in seen.items():
            if len(matches) == 1:
                resolved_results.append(matches[0])
            else:
                duplicate_count += len(matches) - 1
                if policy == "KEEP_FIRST":
                    resolved_results.append(matches[0])
                elif policy == "KEEP_LAST":
                    resolved_results.append(matches[-1])
                elif policy == "KEEP_HIGHEST_CONFIDENCE":
                    # Determine confidence from custom_attributes or a metadata field if present, defaulting to 1.0
                    def get_confidence(res: MatchResult) -> float:
                        conf = res.metadata.custom_attributes.get("confidence")
                        if conf is not None:
                            try:
                                return float(conf)
                            except (TypeError, ValueError):
                                pass
                        return getattr(res, "confidence", 1.0)
                    
                    best = max(matches, key=get_confidence)
                    resolved_results.append(best)
                else:
                    resolved_results.append(matches[0])

        return resolved_results, duplicate_count
