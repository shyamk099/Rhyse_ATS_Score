"""Tests for recommendation models.

Purpose:
    Verify immutability and attribute constraints of Pydantic DTO models.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult
from tests.recommendation.helpers import (
    make_dummy_recommendation,
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
)


class RecommendationModelsTests(unittest.TestCase):
    """Test suite validating DTO model frozen structures."""

    def test_recommendation_is_frozen(self) -> None:
        """Recommendation DTO must be immutable and reject attribute modifications."""
        rec = make_dummy_recommendation()
        with self.assertRaises(Exception):
            rec.priority = 10  # type: ignore[misc]

    def test_recommendation_result_is_frozen(self) -> None:
        """RecommendationResult DTO must be immutable."""
        from tests.recommendation.helpers import make_recommendation_context
        ctx = make_recommendation_context()

        result = RecommendationResult(
            context=ctx,
            recommendations=(),
            statistics={},
            metadata={},
        )
        with self.assertRaises(Exception):
            result.metadata = {"new": "value"}  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
