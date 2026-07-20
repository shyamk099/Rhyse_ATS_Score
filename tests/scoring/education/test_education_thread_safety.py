"""Concurrency tests for the EducationScorer.

Purpose:
    Verify thread safety and isolation when executing EducationScorer pipeline runs.
"""

from __future__ import annotations

import threading
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.education.scorer import EducationScorer
from tests.scoring.education.test_education_scorer import make_mock_edu_result


class EducationThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety under concurrent scoring queries."""

    def test_concurrent_education_scoring(self) -> None:
        registry = ScoringRegistry()
        registry.register("EDUCATION", EducationScorer, priority=300, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_edu_result("M-1", "BSc", "BSc", match_type="EXACT_MATCH"),
            make_mock_edu_result("M-2", "MSc", "MSc", match_type="RELATED_FIELD"),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()

        errors: list[Exception] = []
        outputs: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            try:
                res = pipeline.execute(col, rules)
                self.assertIsNotNone(res)
                self.assertEqual(6.5, res.education_score.raw_score)
                with lock:
                    outputs.append(res.model_dump_json())
            except Exception as e:
                with lock:
                    errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Concurrency errors encountered: {errors}")
        self.assertEqual(100, len(outputs))
