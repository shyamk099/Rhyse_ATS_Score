"""Determinism tests for the ExperienceScorer.

Purpose:
    Verify that 1000 executions yield structurally identical serialized DTO hashes.
"""

from __future__ import annotations

import hashlib
import json
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result


class ExperienceDeterminismTests(unittest.TestCase):
    """Test suite validating determinism of the Experience Scoring pipeline."""

    def test_scoring_determinism(self) -> None:
        registry = ScoringRegistry()
        registry.register("EXPERIENCE", ExperienceScorer, priority=200, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_exp_result("M-1", "Manager", "Manager", match_type="EXACT_MATCH"),
            make_mock_exp_result("M-2", "Developer", "Developer", match_type="PARTIAL_MATCH"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()

        hashes: set[str] = set()

        for _ in range(1000):
            res = pipeline.execute(col, rules)
            data = res.model_dump_json()

            data_dict = json.loads(data)
            data_dict["metadata"]["generated_at"] = "2026-07-19T00:00:00Z"
            data_dict["metadata"]["processing_time_ms"] = 0.0
            data_dict["statistics"]["processing_time_ms"] = 0.0

            normalized_json = json.dumps(data_dict, sort_keys=True)
            sha = hashlib.sha256(normalized_json.encode("utf-8")).hexdigest()
            hashes.add(sha)

        self.assertEqual(1, len(hashes), f"Non-deterministic execution detected! Generated {len(hashes)} different hashes: {hashes}")
