"""Tests for OverallScoreAggregator.

Purpose:
    Verify aggregator correctly normalizes, weights, clamps, populates
    overall_score, and returns a new frozen ScoreResult without mutation.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.exceptions import AggregationValidationError

from tests.scoring.aggregation.helpers import (
    make_score_result,
    make_perfect_score_result,
    make_zero_score_result,
    make_section,
    make_metadata,
    make_statistics,
)


class OverallScoreAggregatorTests(unittest.TestCase):
    """Test suite for OverallScoreAggregator.aggregate()."""

    def setUp(self) -> None:
        self.aggregator = OverallScoreAggregator()

    # ------------------------------------------------------------------
    # Core correctness
    # ------------------------------------------------------------------

    def test_aggregate_returns_score_result(self) -> None:
        """aggregate() must return a ScoreResult instance."""
        result = self.aggregator.aggregate(make_score_result())
        self.assertIsInstance(result, ScoreResult)

    def test_perfect_resume_scores_100(self) -> None:
        """A perfect resume (all sections at max) must yield overall_score == 100.0."""
        result = self.aggregator.aggregate(make_perfect_score_result())
        self.assertAlmostEqual(100.0, result.overall_score, places=6)

    def test_empty_resume_scores_zero(self) -> None:
        """A resume with all zero raw scores must yield overall_score == 0.0."""
        result = self.aggregator.aggregate(make_zero_score_result())
        self.assertAlmostEqual(0.0, result.overall_score, places=6)

    def test_overall_score_is_populated(self) -> None:
        """overall_score must be non-None after aggregation."""
        result = self.aggregator.aggregate(make_score_result())
        self.assertIsNotNone(result.overall_score)
        self.assertIsInstance(result.overall_score, float)

    def test_overall_score_within_bounds(self) -> None:
        """overall_score must be in [0.0, 100.0]."""
        result = self.aggregator.aggregate(make_score_result())
        self.assertGreaterEqual(result.overall_score, 0.0)
        self.assertLessEqual(result.overall_score, 100.0)

    def test_original_score_result_not_mutated(self) -> None:
        """The input ScoreResult must remain unmodified (overall_score stays None)."""
        original = make_score_result()
        self.aggregator.aggregate(original)
        self.assertIsNone(original.overall_score)

    def test_returned_result_is_new_object(self) -> None:
        """The returned ScoreResult must be a different object from the input."""
        original = make_score_result()
        aggregated = self.aggregator.aggregate(original)
        self.assertIsNot(original, aggregated)

    def test_returned_result_is_frozen(self) -> None:
        """The returned ScoreResult must remain frozen after aggregation."""
        result = self.aggregator.aggregate(make_score_result())
        with self.assertRaises(Exception):
            result.overall_score = 0.0  # type: ignore[misc]

    def test_section_scores_preserved_unmodified(self) -> None:
        """SectionScore objects must be carried over unmodified."""
        original = make_score_result(skill_raw=12.0, skill_max=40.0)
        result = self.aggregator.aggregate(original)
        self.assertEqual(12.0, result.skill_score.raw_score)
        self.assertEqual(40.0, result.skill_score.maximum_score)

    # ------------------------------------------------------------------
    # Weighted average formula
    # ------------------------------------------------------------------

    def test_weighted_average_formula_correctness(self) -> None:
        """Verify the exact weighted-average computation against manual calculation."""
        # All sections normalized to 50% (raw == max/2)
        result = self.aggregator.aggregate(make_score_result(
            skill_raw=20.0, skill_max=40.0,       # 50%
            experience_raw=12.5, experience_max=25.0,  # 50%
            education_raw=7.5, education_max=15.0,    # 50%
            project_raw=7.5, project_max=15.0,        # 50%
            certification_raw=5.0, certification_max=10.0,  # 50%
        ))
        # 50 × (0.35 + 0.30 + 0.15 + 0.10 + 0.10) = 50 × 1.0 = 50.0
        self.assertAlmostEqual(50.0, result.overall_score, places=6)

    def test_custom_weights_applied_correctly(self) -> None:
        """Custom weights must be used when provided."""
        # Only skill has a non-zero weight
        weights = SectionWeightConfiguration(
            skill=1.0,
            experience=0.0,
            education=0.0,
            project=0.0,
            certification=0.0,
        )
        agg = OverallScoreAggregator(weight_config=weights)
        result = agg.aggregate(make_score_result(
            skill_raw=20.0, skill_max=40.0,  # 50% normalized → 50.0 × 1.0 = 50.0
            experience_raw=25.0, experience_max=25.0,
            education_raw=15.0, education_max=15.0,
            project_raw=15.0, project_max=15.0,
            certification_raw=10.0, certification_max=10.0,
        ))
        self.assertAlmostEqual(50.0, result.overall_score, places=6)

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    def test_missing_section_raises_aggregation_validation_error(self) -> None:
        """A ScoreResult missing a section must raise AggregationValidationError."""
        from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
        bad_result = ScoreResult(
            skill_score=None,  # missing
            experience_score=make_section("EXPERIENCE", 15.0, 25.0),
            education_score=make_section("EDUCATION", 9.0, 15.0),
            project_score=make_section("PROJECT", 8.0, 15.0),
            certification_score=make_section("CERTIFICATION", 6.0, 10.0),
            statistics=make_statistics(),
            metadata=make_metadata(),
        )
        with self.assertRaises(AggregationValidationError):
            self.aggregator.aggregate(bad_result)

    def test_last_aggregation_stats_populated_after_aggregate(self) -> None:
        """last_aggregation_stats must be non-empty after aggregate()."""
        self.aggregator.aggregate(make_score_result())
        stats = self.aggregator.last_aggregation_stats
        self.assertIn("overall_score", stats)
        self.assertIn("aggregation_time_ms", stats)
        self.assertTrue(stats["aggregation_version"])

    def test_weight_config_property_returns_configuration(self) -> None:
        """weight_config property must return the active SectionWeightConfiguration."""
        agg = OverallScoreAggregator()
        self.assertIsInstance(agg.weight_config, SectionWeightConfiguration)


if __name__ == "__main__":
    unittest.main()
