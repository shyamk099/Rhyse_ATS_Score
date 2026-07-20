"""Unit tests for the Scoring Engine models.

Purpose:
    Verify immutability (frozen=True) and strict schemas (extra='forbid') on DTO models.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary


class ScoringModelsTests(unittest.TestCase):
    """Test suite validating Pydantic rules on models."""

    def test_section_score_immutability(self) -> None:
        score = SectionScore(section_name="SKILL", raw_score=80.0)
        with self.assertRaises((ValidationError, TypeError)):
            score.raw_score = 90.0  # type: ignore

    def test_section_score_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            SectionScore(section_name="SKILL", extra_field="value")  # type: ignore

    def test_score_statistics_immutability(self) -> None:
        stats = ScoreStatistics(total_sections=3)
        with self.assertRaises((ValidationError, TypeError)):
            stats.total_sections = 4  # type: ignore

    def test_score_statistics_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            ScoreStatistics(extra_field="value")  # type: ignore

    def test_score_metadata_immutability(self) -> None:
        meta = ScoreMetadata(engine_version="1", rules_version="1", generated_at="1", pipeline_version="1")
        with self.assertRaises((ValidationError, TypeError)):
            meta.engine_version = "2"  # type: ignore

    def test_score_metadata_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            ScoreMetadata(engine_version="1", rules_version="1", generated_at="1", pipeline_version="1", extra="v")  # type: ignore

    def test_score_result_immutability(self) -> None:
        stats = ScoreStatistics()
        meta = ScoreMetadata(engine_version="1", rules_version="1", generated_at="1", pipeline_version="1")
        res = ScoreResult(statistics=stats, metadata=meta)
        with self.assertRaises((ValidationError, TypeError)):
            res.overall_score = 100.0  # type: ignore

    def test_score_result_forbid_extra(self) -> None:
        stats = ScoreStatistics()
        meta = ScoreMetadata(engine_version="1", rules_version="1", generated_at="1", pipeline_version="1")
        with self.assertRaises(ValidationError):
            ScoreResult(statistics=stats, metadata=meta, extra_field="value")  # type: ignore

    def test_scoring_rules_immutability(self) -> None:
        rules = ScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.version = "1.0.1"  # type: ignore

    def test_scoring_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            ScoringRules(extra_field="value")  # type: ignore
