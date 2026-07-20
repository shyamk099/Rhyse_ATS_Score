"""Tests for ScoringFactory.create_default_explainer().

Purpose:
    Verify factory correctly constructs and wires the explainability engine.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration


class ExplainerFactoryTests(unittest.TestCase):
    """Test suite validating explainer factory creation static method."""

    def test_factory_returns_explainability_engine(self) -> None:
        """create_default_explainer() must return an ExplainabilityEngine."""
        explainer = ScoringFactory.create_default_explainer()
        self.assertIsInstance(explainer, ExplainabilityEngine)

    def test_factory_engine_has_default_weights(self) -> None:
        """Factory engine must fall back to standard weights configuration."""
        explainer = ScoringFactory.create_default_explainer()
        self.assertIsInstance(explainer.weight_config, SectionWeightConfiguration)
        self.assertEqual(0.35, explainer.weight_config.skill)

    def test_factory_engine_with_custom_weights(self) -> None:
        """Factory engine must use custom injected weights configuration."""
        custom = SectionWeightConfiguration(
            skill=0.50, experience=0.20, education=0.10,
            project=0.10, certification=0.10,
        )
        explainer = ScoringFactory.create_default_explainer(weight_config=custom)
        self.assertEqual(0.50, explainer.weight_config.skill)


if __name__ == "__main__":
    unittest.main()
