"""RecommendationMetadataBuilder definition.

Purpose:
    Compile recommendation execution metadata as a plain dict.
"""

from __future__ import annotations

import datetime
from typing import Any


class RecommendationMetadataBuilder:
    """Builder generating metadata records for recommendation executions."""

    @staticmethod
    def build(
        recommendation_version: str = "1.0.0",
        framework_version: str = "1.0.0",
        pipeline_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """Create metadata dict.

        Args:
            recommendation_version: Version of the recommendation engine.
            framework_version: Version of the overall framework.
            pipeline_version: Version of the scoring pipeline.

        Returns:
            A plain dict with versioning and timestamp metadata.
        """
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        return {
            "recommendation_version": recommendation_version,
            "framework_version": framework_version,
            "pipeline_version": pipeline_version,
            "timestamp": now_str,
        }
