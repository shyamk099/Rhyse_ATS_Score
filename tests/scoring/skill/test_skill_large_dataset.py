"""Performance unit tests checking large skill datasets.

Purpose:
    Verify that processing 1000 matched skill features executes within latency targets.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from tests.scoring.skill.test_skill_scorer import make_mock_result


class SkillLargeDatasetTests(unittest.TestCase):
    """Test suite validating performance under large features counts."""

    def test_large_dataset_scoring_latency(self) -> None:
        registry = ScoringRegistry()
        registry.register("SKILL", SkillScorer, priority=100, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        # 1000 matched skills
        results = [
            make_mock_result(f"M-{i}", f"Python-{i}", f"Python-{i}", is_mandatory=(i % 2 == 0))
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
        self.assertEqual("SKILL", res.skill_score.section_name)
        # Weighting: 500 mandatory * 2.0 + 500 optional * 1.0 = 1500.0 clamped to maximum score 40.0
        self.assertEqual(40.0, res.skill_score.raw_score)
        
        # Verify latency is reasonable (typically < 20ms)
        self.assertLess(duration_ms, 100.0, f"Latency target exceeded: took {duration_ms} ms")
