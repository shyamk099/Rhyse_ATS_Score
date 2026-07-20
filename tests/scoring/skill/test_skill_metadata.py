"""Unit tests for the metadata of the SkillScorer.

Purpose:
    Verify that metadata has correct keys, engine version, and timestamp.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules


class SkillMetadataTests(unittest.TestCase):
    """Test suite validating SkillScorer metadata fields."""

    def test_metadata_keys(self) -> None:
        scorer = SkillScorer()
        meta = scorer.metadata()

        self.assertIn("engine_version", meta)
        self.assertIn("rules_version", meta)
        self.assertIn("pipeline_version", meta)
        self.assertEqual("1.0.0", meta["engine_version"])
