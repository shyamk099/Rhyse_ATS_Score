"""Tests for explainability models.

Purpose:
    Verify immutability and attribute validations of the Pydantic DTO models.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.models import (
    SectionExplanation,
    OverallExplanation,
    ExplainabilityResult,
)
from tests.scoring.explainability.helpers import make_score_result


class ExplainabilityModelsTests(unittest.TestCase):
    """Tests checking Pydantic frozen model integrity."""

    def test_section_explanation_is_frozen(self) -> None:
        """SectionExplanation DTO must be immutable."""
        explanation = SectionExplanation(
            section_name="SKILL",
            raw_score=10.0,
            maximum_score=20.0,
            normalized_score=50.0,
            weight_used=0.35,
            formula="...",
            summary="...",
        )
        with self.assertRaises(Exception):
            explanation.raw_score = 15.0  # type: ignore[misc]

    def test_overall_explanation_is_frozen(self) -> None:
        """OverallExplanation DTO must be immutable."""
        explanation = OverallExplanation(
            overall_score=75.0,
            formula="...",
            weight_configuration_version="1.0.0",
            summary="...",
        )
        with self.assertRaises(Exception):
            explanation.overall_score = 90.0  # type: ignore[misc]

    def test_explainability_result_is_frozen(self) -> None:
        """ExplainabilityResult DTO must be immutable."""
        res = ExplainabilityResult(
            score_result=make_score_result(),
            section_explanations={},
            statistics={},
            metadata={},
        )
        with self.assertRaises(Exception):
            res.metadata = {"new": "val"}  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
