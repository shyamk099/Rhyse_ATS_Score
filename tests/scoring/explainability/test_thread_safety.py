"""Tests for thread-safe concurrent score explainability.

Purpose:
    Verify that multiple threads can invoke ExplainabilityEngine.explain()
    concurrently without corruption or shared state leakage.
"""

from __future__ import annotations

import threading
import unittest
from typing import Any

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from ats_engine.domain.ats_scoring.explainability.models import ExplainabilityResult
from tests.scoring.explainability.helpers import make_score_result


class ExplainabilityThreadSafetyTests(unittest.TestCase):
    """Tests checking concurrent execution safety."""

    THREAD_COUNT: int = 20

    def test_concurrent_explains_produce_valid_results(self) -> None:
        """All threads executing explain() concurrently must return correct independent DTOs."""
        engine = ExplainabilityEngine()
        score_result = make_score_result()
        results: list[Any] = [None] * self.THREAD_COUNT
        errors: list[Exception] = []

        def run(index: int) -> None:
            try:
                results[index] = engine.explain(score_result)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(0, len(errors), f"Thread errors: {errors}")
        for r in results:
            self.assertIsInstance(r, ExplainabilityResult)
            self.assertIsNotNone(r.overall_explanation)

    def test_concurrent_results_have_unique_identities(self) -> None:
        """Concurrently generated ExplainabilityResult wraps must have unique memory ids."""
        engine = ExplainabilityEngine()
        score_result = make_score_result()
        results: list[Any] = [None] * self.THREAD_COUNT

        def run(index: int) -> None:
            results[index] = engine.explain(score_result)

        threads = [threading.Thread(target=run, args=(i,)) for i in range(self.THREAD_COUNT)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        ids = {id(r) for r in results if r is not None}
        self.assertEqual(self.THREAD_COUNT, len(ids))


if __name__ == "__main__":
    unittest.main()
