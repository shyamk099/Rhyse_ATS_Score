"""Tests for orchestration metadata correctness.

Purpose:
    Verify that ScoreResult.metadata is correctly populated with pipeline_version,
    generated_at, engine_version, and milestone after orchestration.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator

from tests.scoring.orchestrator.helpers import make_collection, make_scorer


class OrchestratorMetadataTests(unittest.TestCase):
    """Tests verifying metadata fields are populated after orchestrate()."""

    def _make_orchestrator(self) -> ScoreOrchestrator:
        return ScoringFactory.create_default_orchestrator()

    def test_metadata_is_not_none(self) -> None:
        """result.metadata must be populated after orchestration."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertIsNotNone(result.metadata)

    def test_metadata_pipeline_version_is_set(self) -> None:
        """metadata.pipeline_version must be a non-empty string."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertIsInstance(result.metadata.pipeline_version, str)
        self.assertTrue(result.metadata.pipeline_version)

    def test_metadata_generated_at_is_set(self) -> None:
        """metadata.generated_at must be a non-empty ISO timestamp string."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertIsInstance(result.metadata.generated_at, str)
        self.assertGreater(len(result.metadata.generated_at), 0)
        self.assertIn("T", result.metadata.generated_at)

    def test_metadata_engine_version_is_set(self) -> None:
        """metadata.engine_version must be a non-empty version string."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertIsInstance(result.metadata.engine_version, str)
        self.assertTrue(result.metadata.engine_version)

    def test_metadata_processing_time_ms_is_positive(self) -> None:
        """metadata.processing_time_ms must be a non-negative float."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertGreaterEqual(result.metadata.processing_time_ms, 0.0)

    def test_metadata_rules_version_is_set(self) -> None:
        """metadata.rules_version must reflect the active ScoringRules version."""
        result = self._make_orchestrator().orchestrate(make_collection())
        self.assertIsInstance(result.metadata.rules_version, str)
        self.assertTrue(result.metadata.rules_version)

    def test_orchestration_stats_execution_time_is_positive(self) -> None:
        """Orchestration stats execution_time_ms must be >= 0."""
        orch = self._make_orchestrator()
        orch.orchestrate(make_collection())
        stats = orch.last_orchestration_stats
        self.assertGreaterEqual(stats["execution_time_ms"], 0.0)

    def test_orchestration_stats_pipeline_version_is_set(self) -> None:
        """Orchestration stats must include a non-empty pipeline_version string."""
        orch = self._make_orchestrator()
        orch.orchestrate(make_collection())
        stats = orch.last_orchestration_stats
        self.assertIsInstance(stats["pipeline_version"], str)
        self.assertTrue(stats["pipeline_version"])

    def test_metadata_populated_for_custom_registry(self) -> None:
        """Metadata must be correctly set even with a custom minimal registry."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        pipeline = ScoringPipeline(registry=reg)
        orch = ScoreOrchestrator(pipeline=pipeline, registry=reg)
        result = orch.orchestrate(make_collection())
        self.assertIsNotNone(result.metadata)
        self.assertTrue(result.metadata.pipeline_version)


if __name__ == "__main__":
    unittest.main()
