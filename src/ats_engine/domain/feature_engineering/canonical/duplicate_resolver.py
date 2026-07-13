"""Duplicate resolver for canonical features.

Purpose:
    Filter duplicate feature entries with identical feature_ids based on a policy:
    KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL.
"""

from __future__ import annotations

from typing import Sequence
from ats_engine.domain.feature_engineering.exceptions import DuplicateFeatureError
from ats_engine.domain.feature_engineering.models import Feature


class DuplicateFeatureResolver:
    """Duplicate resolver utilizing configured policies to deduplicate features."""

    def resolve(
        self,
        features: Sequence[Feature],
        policy: str,
    ) -> tuple[Sequence[Feature], int]:
        """Deduplicate features with identical feature_ids according to policy.

        Args:
            features: Sequence of Feature objects.
            policy: One of KEEP_FIRST, KEEP_LAST, KEEP_HIGHEST_CONFIDENCE, KEEP_ALL.

        Returns:
            A tuple of (deduplicated_features_list, duplicate_count).

        Raises:
            DuplicateFeatureError: If policy value is unknown or unsupported.
        """
        valid_policies = {"KEEP_FIRST", "KEEP_LAST", "KEEP_HIGHEST_CONFIDENCE", "KEEP_ALL"}
        if policy not in valid_policies:
            raise DuplicateFeatureError(f"Unsupported duplicate resolution policy: '{policy}'")

        if policy == "KEEP_ALL":
            return features, 0

        # Group by feature_id
        grouped: dict[str, list[Feature]] = {}
        for f in features:
            grouped.setdefault(f.feature_id, []).append(f)

        resolved: list[Feature] = []
        duplicate_count = 0

        for fid, occurrences in grouped.items():
            if len(occurrences) > 1:
                duplicate_count += (len(occurrences) - 1)

            if policy == "KEEP_FIRST":
                resolved.append(occurrences[0])
            elif policy == "KEEP_LAST":
                resolved.append(occurrences[-1])
            elif policy == "KEEP_HIGHEST_CONFIDENCE":
                # Find maximum confidence, retaining original stable index if tied
                best = max(occurrences, key=lambda x: x.confidence)
                resolved.append(best)

        return resolved, duplicate_count
