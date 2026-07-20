"""Tests for ExplainabilityEngine.

Purpose:
    Verify explainer correctly orchestrates section and overall explanations,
    honours optionality of overall_score, and validates input result structure.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult
from ats_engine.domain.ats_scoring.exceptions import ExplainabilityValidationError
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult

from tests.scoring.explainability.helpers import (
    make_score_result,
    make_perfect_score_result,
    make_zero_score_result,
    make_section,
    make_metadata,
    make_statistics,
)


class ExplainabilityEngineTests(unittest.TestCase):
    """Test suite validating ExplainabilityEngine execution workflow."""

    def setUp(self) -> None:
        self.engine = ExplainabilityEngine()

    def test_explain_returns_explainability_result(self) -> None:
        """explain() must return a valid ExplainabilityResult wrapper DTO."""
        res = self.engine.explain(make_score_result())
        self.assertIsInstance(res, ExplainabilityResult)

    def test_wraps_score_result(self) -> None:
        """The returned ExplainabilityResult must wrap the original ScoreResult."""
        sr = make_score_result()
        res = self.engine.explain(sr)
        self.assertIs(sr, res.score_result)

    def test_overall_score_populated_generates_overall_explanation(self) -> None:
        """If overall_score is populated, overall_explanation must not be None."""
        sr = make_score_result(overall_score=82.4)
        res = self.engine.explain(sr)
        self.assertIsNotNone(res.overall_explanation)
        self.assertEqual(82.4, res.overall_explanation.overall_score)

    def test_overall_score_none_skips_overall_explanation(self) -> None:
        """If overall_score is None, overall_explanation must be None (relaxed validation)."""
        sr = make_score_result(overall_score=None)
        res = self.engine.explain(sr)
        self.assertIsNone(res.overall_explanation)
        # Should still explain all 5 sections
        self.assertEqual(5, len(res.section_explanations))

    def test_perfect_score_aggregation_explanations(self) -> None:
        """Perfect resume must generate maximum scoring explanations."""
        sr = make_perfect_score_result()
        res = self.engine.explain(sr)
        self.assertEqual(100.0, res.overall_explanation.overall_score)
        self.assertEqual(100.0, res.section_explanations["SKILL"].normalized_score)

    def test_zero_score_aggregation_explanations(self) -> None:
        """Zero score resume must yield zeroed explanations."""
        sr = make_zero_score_result()
        res = self.engine.explain(sr)
        self.assertEqual(0.0, res.overall_explanation.overall_score)
        self.assertEqual(0.0, res.section_explanations["SKILL"].normalized_score)

    def test_missing_section_raises_validation_error(self) -> None:
        """If any required section scorer result is missing, raise validation error."""
        bad_sr = ScoreResult(
            skill_score=None,  # missing
            experience_score=make_section("EXPERIENCE"),
            education_score=make_section("EDUCATION"),
            project_score=make_section("PROJECT"),
            certification_score=make_section("CERTIFICATION"),
            metadata=make_metadata(),
            statistics=make_statistics(),
        )
        with self.assertRaises(ExplainabilityValidationError):
            self.engine.explain(bad_sr)

    def test_none_raw_score_raises_validation_error(self) -> None:
        """If any section score has raw_score=None, raise validation error."""
        bad_sr = ScoreResult(
            skill_score=make_section("SKILL", raw_score=None),  # None raw
            experience_score=make_section("EXPERIENCE"),
            education_score=make_section("EDUCATION"),
            project_score=make_section("PROJECT"),
            certification_score=make_section("CERTIFICATION"),
            metadata=make_metadata(),
            statistics=make_statistics(),
        )
        with self.assertRaises(ExplainabilityValidationError):
            self.engine.explain(bad_sr)

    def test_none_maximum_score_raises_validation_error(self) -> None:
        """If any section score has maximum_score=None or <= 0, raise validation error."""
        bad_sr = ScoreResult(
            skill_score=make_section("SKILL", maximum_score=0.0),  # zero max
            experience_score=make_section("EXPERIENCE"),
            education_score=make_section("EDUCATION"),
            project_score=make_section("PROJECT"),
            certification_score=make_section("CERTIFICATION"),
            metadata=make_metadata(),
            statistics=make_statistics(),
        )
        with self.assertRaises(ExplainabilityValidationError):
            self.engine.explain(bad_sr)

    def test_last_aggregation_stats_populated(self) -> None:
        """Telemetry statistics must be returned inside ExplainabilityResult."""
        res = self.engine.explain(make_score_result())
        self.assertIsNotNone(res.statistics)
        self.assertIn("execution_time_ms", res.statistics)
        self.assertEqual(5, len(res.statistics["sections_processed"]))

    def test_metadata_populated(self) -> None:
        """Metadata fields must be populated on result."""
        res = self.engine.explain(make_score_result())
        self.assertIsNotNone(res.metadata)
        self.assertEqual("1.0.0", res.metadata["explainability_version"])


if __name__ == "__main__":
    unittest.main()
