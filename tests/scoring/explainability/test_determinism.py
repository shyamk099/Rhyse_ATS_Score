"""Tests for explainability determinism.

Purpose:
    Verify that repeated explain() calls on the same ScoreResult produce
    identical outputs (formulas, summaries, and stats fields) across repetitions.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from tests.scoring.explainability.helpers import make_score_result


class ExplainabilityDeterminismTests(unittest.TestCase):
    """Tests checking deterministic explanation output consistency."""

    REPETITIONS: int = 25

    def setUp(self) -> None:
        self.engine = ExplainabilityEngine()
        self.score_result = make_score_result()

    def test_explain_is_fully_deterministic(self) -> None:
        """Repeated explain() calls must return identical formula and summary strings."""
        first = self.engine.explain(self.score_result)
        for _ in range(self.REPETITIONS - 1):
            res = self.engine.explain(self.score_result)
            self.assertEqual(first.overall_explanation.formula, res.overall_explanation.formula)
            self.assertEqual(first.overall_explanation.summary, res.overall_explanation.summary)
            for k in ["SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"]:
                self.assertEqual(
                    first.section_explanations[k].formula,
                    res.section_explanations[k].formula,
                )
                self.assertEqual(
                    first.section_explanations[k].summary,
                    res.section_explanations[k].summary,
                )


if __name__ == "__main__":
    unittest.main()
