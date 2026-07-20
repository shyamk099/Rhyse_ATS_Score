"""Tests for RecommendationValidator.

Purpose:
    Verify validation checks for inputs and provider priorities.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.validator import RecommendationValidator
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError
from tests.recommendation.helpers import (
    DummyProvider,
    make_mock_match_collection,
    make_mock_score_result,
    make_mock_explainability_result,
)


class RecommendationValidatorTests(unittest.TestCase):
    """Test suite validating inputs and registry constraints."""

    def setUp(self) -> None:
        self.match_collection = make_mock_match_collection()
        self.score_result = make_mock_score_result()
        self.explainability_result = make_mock_explainability_result(self.score_result)
        self.registry = RecommendationRegistry()

    def test_inputs_validation_with_none_raises_validation_error(self) -> None:
        """Any None input must trigger RecommendationValidationError."""
        with self.assertRaises(RecommendationValidationError):
            RecommendationValidator.validate_inputs(None)

        from ats_engine.domain.recommendation.models import RecommendationContext
        bad_ctx = RecommendationContext(
            match_collection=None,  # type: ignore[arg-type]
            score_result=self.score_result,
            explainability_result=self.explainability_result,
        )
        with self.assertRaises(RecommendationValidationError):
            RecommendationValidator.validate_inputs(bad_ctx)

    def test_valid_inputs_pass(self) -> None:
        """Valid non-None inputs must pass validation silently."""
        from tests.recommendation.helpers import make_recommendation_context
        RecommendationValidator.validate_inputs(make_recommendation_context())

    def test_registry_with_duplicate_priorities_raises_validation_error(self) -> None:
        """Two providers with the same priority value must raise RecommendationValidationError."""
        self.registry.register(DummyProvider(name="SKILL", priority_val=10))
        self.registry.register(DummyProvider(name="EXPERIENCE", priority_val=10))

        with self.assertRaises(RecommendationValidationError) as ctx:
            RecommendationValidator.validate_registry(self.registry)
        self.assertIn("share the same priority", str(ctx.exception))

    def test_valid_registry_passes(self) -> None:
        """Registry with unique priorities must pass validation silently."""
        self.registry.register(DummyProvider(name="SKILL", priority_val=10))
        self.registry.register(DummyProvider(name="EXPERIENCE", priority_val=20))
        RecommendationValidator.validate_registry(self.registry)


if __name__ == "__main__":
    unittest.main()
