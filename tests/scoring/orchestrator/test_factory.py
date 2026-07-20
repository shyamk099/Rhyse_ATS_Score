"""Tests for ScoringFactory.create_default_orchestrator().

Purpose:
    Verify factory produces a correctly wired ScoreOrchestrator and
    that all five default scorers are registered and functional.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult

from tests.scoring.orchestrator.helpers import make_collection


class OrchestratorFactoryTests(unittest.TestCase):
    """Tests for ScoringFactory.create_default_orchestrator()."""

    def test_factory_returns_score_orchestrator(self) -> None:
        """create_default_orchestrator() must return a ScoreOrchestrator."""
        orch = ScoringFactory.create_default_orchestrator()
        self.assertIsInstance(orch, ScoreOrchestrator)

    def test_factory_orchestrator_has_pipeline(self) -> None:
        """Orchestrator returned by factory must have a ScoringPipeline."""
        orch = ScoringFactory.create_default_orchestrator()
        self.assertIsInstance(orch.pipeline, ScoringPipeline)

    def test_factory_orchestrator_has_registry(self) -> None:
        """Orchestrator returned by factory must have a ScoringRegistry."""
        orch = ScoringFactory.create_default_orchestrator()
        self.assertIsInstance(orch.registry, ScoringRegistry)

    def test_factory_registry_has_five_scorers(self) -> None:
        """Default orchestrator registry must contain exactly the five standard scorers."""
        orch = ScoringFactory.create_default_orchestrator()
        names = set(orch.registry.list())
        self.assertEqual(
            {"SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"}, names
        )

    def test_factory_orchestrator_can_orchestrate(self) -> None:
        """Factory orchestrator must successfully orchestrate a minimal collection."""
        orch = ScoringFactory.create_default_orchestrator()
        result = orch.orchestrate(make_collection())
        self.assertIsInstance(result, ScoreResult)

    def test_factory_with_custom_registry(self) -> None:
        """create_default_orchestrator() must accept an injected registry."""
        from tests.scoring.orchestrator.helpers import make_scorer
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        orch = ScoringFactory.create_default_orchestrator(registry=reg)
        self.assertIs(reg, orch.registry)

    def test_factory_with_none_registry_creates_default(self) -> None:
        """create_default_orchestrator(registry=None) must create a default registry."""
        orch = ScoringFactory.create_default_orchestrator(registry=None)
        self.assertIsInstance(orch.registry, ScoringRegistry)
        self.assertGreater(len(orch.registry.list()), 0)

    def test_factory_create_default_registry_is_importable(self) -> None:
        """ScoringFactory must expose create_default_orchestrator as a static method."""
        self.assertTrue(callable(ScoringFactory.create_default_orchestrator))

    def test_factory_orchestrate_overall_score_is_none(self) -> None:
        """Factory orchestrator must not compute an overall_score."""
        orch = ScoringFactory.create_default_orchestrator()
        result = orch.orchestrate(make_collection())
        self.assertIsNone(result.overall_score)


if __name__ == "__main__":
    unittest.main()
