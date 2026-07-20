"""Performance unit tests checking large certification datasets.

Purpose:
    Verify that processing 1000 matched certification features executes within latency targets.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.certification.scorer import CertificationScorer
from tests.scoring.certification.test_certification_scorer import make_mock_cert_result


class CertificationLargeDatasetTests(unittest.TestCase):
    """Test suite validating performance under large features counts."""

    def test_large_dataset_scoring_latency(self) -> None:
        registry = ScoringRegistry()
        registry.register("CERTIFICATION", CertificationScorer, priority=500, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        # 1000 matched certifications
        results = [
            make_mock_cert_result(f"M-{i}", f"Cert-{i}", f"Cert-{i}", match_type="EXACT_MATCH" if i % 2 == 0 else "EQUIVALENT_CERTIFICATION")
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
        self.assertEqual("CERTIFICATION", res.certification_score.section_name)
        # Weighting: 500 exact (3.0) + 500 equivalent (2.5) = 2750.0 clamped to maximum score 10.0
        self.assertEqual(10.0, res.certification_score.raw_score)
        
        # Verify latency is reasonable (typically < 20ms, allow up to 100ms for CI)
        self.assertLess(duration_ms, 100.0, f"Latency target exceeded: took {duration_ms} ms")
