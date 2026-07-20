"""Tests for ScoreNormalizer.

Purpose:
    Verify the normalization formula, clamping, None handling,
    and error cases for zero/None maximum_score.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.normalization import ScoreNormalizer
from ats_engine.domain.ats_scoring.exceptions import NormalizationError

from tests.scoring.aggregation.helpers import make_section, make_score_result


class ScoreNormalizerTests(unittest.TestCase):
    """Tests for ScoreNormalizer.normalize() and normalize_all()."""

    # ------------------------------------------------------------------
    # normalize() — single section
    # ------------------------------------------------------------------

    def test_normalize_50_percent(self) -> None:
        """10 / 20 × 100 must equal 50.0."""
        section = make_section("SKILL", raw_score=10.0, maximum_score=20.0)
        self.assertAlmostEqual(50.0, ScoreNormalizer.normalize(section), places=6)

    def test_normalize_100_percent(self) -> None:
        """max / max × 100 must equal 100.0."""
        section = make_section("SKILL", raw_score=40.0, maximum_score=40.0)
        self.assertAlmostEqual(100.0, ScoreNormalizer.normalize(section), places=6)

    def test_normalize_zero_raw(self) -> None:
        """0 / max × 100 must equal 0.0."""
        section = make_section("SKILL", raw_score=0.0, maximum_score=40.0)
        self.assertAlmostEqual(0.0, ScoreNormalizer.normalize(section), places=6)

    def test_normalize_arbitrary_values(self) -> None:
        """12 / 15 × 100 must equal 80.0."""
        section = make_section("EDUCATION", raw_score=12.0, maximum_score=15.0)
        self.assertAlmostEqual(80.0, ScoreNormalizer.normalize(section), places=6)

    def test_normalize_clamps_above_100(self) -> None:
        """raw > maximum must clamp to 100.0."""
        section = make_section("SKILL", raw_score=50.0, maximum_score=40.0)
        result = ScoreNormalizer.normalize(section)
        self.assertAlmostEqual(100.0, result, places=6)

    def test_normalize_clamps_below_zero(self) -> None:
        """Negative raw_score (edge case) must clamp to 0.0."""
        from ats_engine.domain.ats_scoring.models.section_score import SectionScore
        section = SectionScore(section_name="SKILL", raw_score=-5.0, maximum_score=40.0)
        result = ScoreNormalizer.normalize(section)
        self.assertAlmostEqual(0.0, result, places=6)

    def test_normalize_none_raw_treated_as_zero(self) -> None:
        """None raw_score must be treated as 0.0 (not raise)."""
        from ats_engine.domain.ats_scoring.models.section_score import SectionScore
        section = SectionScore(section_name="SKILL", raw_score=None, maximum_score=40.0)
        result = ScoreNormalizer.normalize(section)
        self.assertAlmostEqual(0.0, result, places=6)

    def test_normalize_zero_maximum_raises(self) -> None:
        """maximum_score == 0 must raise NormalizationError."""
        from ats_engine.domain.ats_scoring.models.section_score import SectionScore
        section = SectionScore(section_name="SKILL", raw_score=10.0, maximum_score=0.0)
        with self.assertRaises(NormalizationError):
            ScoreNormalizer.normalize(section)

    def test_normalize_none_maximum_raises(self) -> None:
        """maximum_score == None must raise NormalizationError."""
        from ats_engine.domain.ats_scoring.models.section_score import SectionScore
        section = SectionScore(section_name="SKILL", raw_score=10.0, maximum_score=None)
        with self.assertRaises(NormalizationError):
            ScoreNormalizer.normalize(section)

    def test_normalize_error_message_contains_section_name(self) -> None:
        """NormalizationError must name the offending section."""
        from ats_engine.domain.ats_scoring.models.section_score import SectionScore
        section = SectionScore(section_name="CERTIFICATION", raw_score=5.0, maximum_score=0.0)
        with self.assertRaises(NormalizationError) as ctx:
            ScoreNormalizer.normalize(section)
        self.assertIn("CERTIFICATION", str(ctx.exception))

    # ------------------------------------------------------------------
    # normalize_all() — full ScoreResult
    # ------------------------------------------------------------------

    def test_normalize_all_returns_five_keys(self) -> None:
        """normalize_all() must return exactly 5 section entries."""
        normalized = ScoreNormalizer.normalize_all(make_score_result())
        self.assertEqual(5, len(normalized))

    def test_normalize_all_correct_keys(self) -> None:
        """normalize_all() dict must contain all five section names."""
        normalized = ScoreNormalizer.normalize_all(make_score_result())
        expected = {"SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"}
        self.assertEqual(expected, set(normalized.keys()))

    def test_normalize_all_values_in_range(self) -> None:
        """All normalized values must be in [0.0, 100.0]."""
        normalized = ScoreNormalizer.normalize_all(make_score_result())
        for name, value in normalized.items():
            self.assertGreaterEqual(value, 0.0, f"{name} < 0")
            self.assertLessEqual(value, 100.0, f"{name} > 100")

    def test_normalize_all_perfect_scores_all_100(self) -> None:
        """Perfect score result must normalize all sections to 100.0."""
        from tests.scoring.aggregation.helpers import make_perfect_score_result
        normalized = ScoreNormalizer.normalize_all(make_perfect_score_result())
        for name, value in normalized.items():
            self.assertAlmostEqual(100.0, value, places=6, msg=f"{name} != 100")

    def test_normalize_all_zero_scores_all_zero(self) -> None:
        """Zero score result must normalize all sections to 0.0."""
        from tests.scoring.aggregation.helpers import make_zero_score_result
        normalized = ScoreNormalizer.normalize_all(make_zero_score_result())
        for name, value in normalized.items():
            self.assertAlmostEqual(0.0, value, places=6, msg=f"{name} != 0")

    def test_normalize_all_missing_section_raises(self) -> None:
        """normalize_all() must raise NormalizationError if a section is None."""
        from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
        from tests.scoring.aggregation.helpers import make_metadata, make_statistics, make_section
        bad = ScoreResult(
            skill_score=None,
            experience_score=make_section("EXPERIENCE", 15.0, 25.0),
            education_score=make_section("EDUCATION", 9.0, 15.0),
            project_score=make_section("PROJECT", 8.0, 15.0),
            certification_score=make_section("CERTIFICATION", 6.0, 10.0),
            statistics=make_statistics(),
            metadata=make_metadata(),
        )
        with self.assertRaises(NormalizationError):
            ScoreNormalizer.normalize_all(bad)


if __name__ == "__main__":
    unittest.main()
