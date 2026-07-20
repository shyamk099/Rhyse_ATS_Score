"""Tests for formula and contribution mathematical correctness.

Purpose:
    Verify formula arithmetic generation values match mathematical criteria.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from tests.scoring.explainability.helpers import make_score_result


class ExplainabilityFormulaTests(unittest.TestCase):
    """Test suite validating section contribution formulas and overall summation formatting."""

    def setUp(self) -> None:
        self.engine = ExplainabilityEngine()

    def test_section_score_contribution_calculation(self) -> None:
        """Verify the arithmetic normalization and weighting is represented correctly."""
        sr = make_score_result(
            skill_raw=17.0, skill_max=20.0,  # 85% normalized
        )
        res = self.engine.explain(sr)

        skill_expl = res.section_explanations["SKILL"]
        self.assertEqual(85.0, skill_expl.normalized_score)
        self.assertEqual(0.35, skill_expl.weight_used)
        # 85 * 0.35 = 29.75
        self.assertEqual("(17 / 20) × 100 × 0.35 = 29.75", skill_expl.formula)

    def test_overall_formula_correctness(self) -> None:
        """Verify overall ATS summation matches contribution additions."""
        sr = make_score_result(
            overall_score=82.40,
            skill_raw=17.0, skill_max=20.0,             # 85% norm * 0.35 = 29.75
            experience_raw=19.0, experience_max=25.0,     # 76% norm * 0.30 = 22.8
            education_raw=15.0, education_max=15.0,       # 100% norm * 0.15 = 15.0
            project_raw=6.9, project_max=10.0,            # 69% norm * 0.10 = 6.9
            certification_raw=7.95, certification_max=10.0, # 79.5% norm * 0.10 = 7.95
        )
        # Sum = 29.75 + 22.8 + 15.0 + 6.9 + 7.95 = 82.4
        res = self.engine.explain(sr)
        self.assertEqual("82.4 = 29.75 + 22.8 + 15 + 6.9 + 7.95", res.overall_explanation.formula)


if __name__ == "__main__":
    unittest.main()
