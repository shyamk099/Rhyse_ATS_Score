"""Concurrency tests for the ProjectScorer.

Purpose:
    Verify thread safety and isolation when executing ProjectScorer pipeline runs.
"""

from __future__ import annotations

import threading
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.project.scorer import ProjectScorer
from tests.scoring.project.test_project_scorer import make_mock_proj_result


class ProjectThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety under concurrent scoring queries."""

    def test_concurrent_project_scoring(self) -> None:
        registry = ScoringRegistry()
        registry.register("PROJECT", ProjectScorer, priority=400, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_proj_result("M-1", "Parser", "Parser", match_type="EXACT_MATCH"),
            make_mock_proj_result("M-2", "Scorer", "Scorer", match_type="SIMILAR_PROJECT"),
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
                self.assertEqual(5.5, res.project_score.raw_score)
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
