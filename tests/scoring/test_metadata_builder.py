"""Unit tests for the ScoreMetadataBuilder.

Purpose:
    Verify metadata compiling and correct version mappings.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.common.metadata_builder import ScoreMetadataBuilder
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata


class ScoreMetadataBuilderTests(unittest.TestCase):
    """Test suite validating ScoreMetadataBuilder behaviors."""

    def test_metadata_builder_populates_correct_dto(self) -> None:
        meta = ScoreMetadataBuilder.build(
            engine_version="1.0.0",
            rules_version="1.0.0",
            pipeline_version="1.0.0",
            processing_time_ms=10.0,
        )

        self.assertIsInstance(meta, ScoreMetadata)
        self.assertEqual("1.0.0", meta.engine_version)
        self.assertEqual("1.0.0", meta.rules_version)
        self.assertEqual("1.0.0", meta.pipeline_version)
        self.assertEqual(10.0, meta.processing_time_ms)
        self.assertEqual("6", meta.book_version)
        self.assertEqual("6.1", meta.milestone)
        self.assertTrue(meta.generated_at.endswith("Z"))
