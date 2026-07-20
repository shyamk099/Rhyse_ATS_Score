"""Performance unit tests checking large experience datasets.

Purpose:
    Verify that processing 1000 matched experience features executes within latency targets.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result


class ExperienceLargeDatasetTests(unittest.TestCase):
    """Test suite validating performance under large features counts."""

    def test_large_dataset_scoring_latency(self) -> None:
        registry = ScoringRegistry()
        registry.register("EXPERIENCE", ExperienceScorer, priority=200, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        # 1000 matched experiences
        results = [
            make_mock_exp_result(f"M-{i}", f"Manager-{i}", f"Manager-{i}", match_type="EXACT_MATCH" if i % 2 == 0 else "PARTIAL_MATCH")
            for i in range(1000)
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()

        start = time.perf_counter()
        res = pipeline.execute(col, rules)
        duration_ms = (time.perf_counter() - start) * 1000.0

        self.assertIsNotNone(res)
        self.assertEqual("EXPERIENCE", res.experience_score.section_name)
        # Weighting: 500 exact (3.0) + 500 partial (1.5) = 2250.0 clamped to maximum score 25.0
        self.assertEqual(25.0, res.experience_score.raw_score)
        
        # Verify latency is reasonable (typically < 20ms)
        self.assertLess(duration_ms, 100.0, f"Latency target exceeded: took {duration_ms} ms")
