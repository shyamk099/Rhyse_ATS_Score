"""ScoreMetadataBuilder definition.

Purpose:
    Expose metadata compiling for scoring pipeline executions.
"""

from __future__ import annotations

import datetime

from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata


class ScoreMetadataBuilder:
    """Builder generating metadata records for scoring pipeline executions."""

    @staticmethod
    def build(
        engine_version: str = "1.0.0",
        rules_version: str = "1.0.0",
        pipeline_version: str = "1.0.0",
        processing_time_ms: float = 0.0,
        book_version: str = "6",
        milestone: str = "6.1",
    ) -> ScoreMetadata:
        """Create a new frozen ScoreMetadata DTO."""
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        return ScoreMetadata(
            engine_version=engine_version,
            rules_version=rules_version,
            generated_at=now_str,
            processing_time_ms=processing_time_ms,
            pipeline_version=pipeline_version,
            book_version=book_version,
            milestone=milestone,
        )

