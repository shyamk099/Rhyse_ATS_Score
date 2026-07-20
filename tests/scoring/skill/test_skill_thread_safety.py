"""Concurrency tests for the SkillScorer.

Purpose:
    Verify thread safety and isolation when executing SkillScorer pipeline runs.
"""

from __future__ import annotations

import threading
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from tests.scoring.skill.test_skill_scorer import make_mock_result


class SkillThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety under concurrent scoring queries."""

    def test_concurrent_skill_scoring(self) -> None:
        registry = ScoringRegistry()
        registry.register("SKILL", SkillScorer, priority=100, enabled=True)
        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_result("M-1", "Python", "Python", is_mandatory=True),
            make_mock_result("M-2", "SQL", "SQL", is_mandatory=False),
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
                self.assertEqual(3.0, res.skill_score.raw_score)
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
