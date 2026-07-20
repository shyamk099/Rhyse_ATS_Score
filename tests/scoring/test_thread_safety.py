"""Concurrency tests for the Scoring Engine.

Purpose:
    Verify thread safety when executing scoring pipeline runs concurrently across threads.
"""

from __future__ import annotations

import threading
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.service import ScoringService
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore


class ThreadSafeDummyScorer(AbstractScorer):
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="SKILL", raw_score=90.0)
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {}
    def metadata(self) -> dict:
        return {}


class ScoringThreadSafetyTests(unittest.TestCase):
    """Test suite validating thread safety of ScoringService and pipeline execution."""

    def test_concurrent_scoring_execution(self) -> None:
        service = ScoringService()
        service.registry.register("SKILL", ThreadSafeDummyScorer)

        collection = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()

        errors: list[Exception] = []
        outputs: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            try:
                res = service.score(collection, rules)
                self.assertIsNotNone(res)
                self.assertEqual(90.0, res.skill_score.raw_score)
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
