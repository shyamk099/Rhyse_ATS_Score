"""Tests for ExplainabilityFormatter.

Purpose:
    Verify format of mathematical calculation strings and summaries.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.formatter import ExplainabilityFormatter
from ats_engine.domain.ats_scoring.exceptions import FormattingError


class ExplainabilityFormatterTests(unittest.TestCase):
    """Test suite validating ExplainabilityFormatter formatting correctness."""

    def test_format_section_formula_standard(self) -> None:
        """Verify formula matches (raw / max) × 100 × weight = contribution."""
        formula = ExplainabilityFormatter.format_section_formula(
            raw_score=17.0,
            maximum_score=20.0,
            weight_used=0.35,
            contribution=29.75,
        )
        self.assertEqual("(17 / 20) × 100 × 0.35 = 29.75", formula)

    def test_format_section_formula_zero_maximum_raises(self) -> None:
        """Formatting with zero maximum_score must raise FormattingError."""
        with self.assertRaises(FormattingError):
            ExplainabilityFormatter.format_section_formula(
                raw_score=10.0,
                maximum_score=0.0,
                weight_used=0.1,
                contribution=1.0,
            )

    def test_format_section_summary(self) -> None:
        """Verify section summary matches the format requirement."""
        summary = ExplainabilityFormatter.format_section_summary(
            section_name="SKILL",
            raw_score=17.0,
            maximum_score=20.0,
            normalized_score=85.0,
            weight_used=0.35,
            matched_count=18,
            missing_count=2,
        )
        self.assertEqual("Skill Score: 17/20 (85%). Matched: 18, Missing: 2.", summary)

    def test_format_overall_formula(self) -> None:
        """Verify overall ATS formula format is constructed correctly."""
        contributions = {
            "SKILL": 29.75,
            "EXPERIENCE": 22.80,
            "EDUCATION": 15.00,
            "PROJECT": 6.90,
            "CERTIFICATION": 7.95,
        }
        formula = ExplainabilityFormatter.format_overall_formula(
            overall_score=82.40,
            contributions=contributions,
        )
        self.assertEqual("82.4 = 29.75 + 22.8 + 15 + 6.9 + 7.95", formula)

    def test_format_overall_summary(self) -> None:
        """Verify overall summary text formatting."""
        summary = ExplainabilityFormatter.format_overall_summary(overall_score=82.40)
        self.assertEqual("Overall ATS Score: 82.40/100.00.", summary)


if __name__ == "__main__":
    unittest.main()
