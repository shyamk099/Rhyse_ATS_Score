"""Performance unit tests checking large education datasets.

Purpose:
    Verify that processing 1000 matched education features executes within latency targets.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.education.scorer import EducationScorer
from tests.scoring.education.test_education_scorer import make_mock_edu_result


class EducationLargeDatasetTests(unittest.TestCase):
    """Test suite validating performance under large features counts."""

    def test_large_dataset_scoring_latency(self) -> None:
        registry = ScoringRegistry()
        registry.register("EDUCATION", EducationScorer, priority=300, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        # 1000 matched educations
        results = [
            make_mock_edu_result(f"M-{i}", f"BSc-{i}", f"BSc-{i}", match_type="EXACT_MATCH" if i % 2 == 0 else "RELATED_FIELD")
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
        self.assertEqual("EDUCATION", res.education_score.section_name)
        # Weighting: 500 exact (4.0) + 500 related (2.5) = 3250.0 clamped to maximum score 15.0
        self.assertEqual(15.0, res.education_score.raw_score)
        
        # Verify latency is reasonable (typically < 20ms)
        self.assertLess(duration_ms, 100.0, f"Latency target exceeded: took {duration_ms} ms")
