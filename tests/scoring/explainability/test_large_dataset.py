"""Tests for performance scale explainability.

Purpose:
    Verify that explaining 1000 score results sequentially completes within 100ms.
"""

from __future__ import annotations

import time
import unittest

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from tests.scoring.explainability.helpers import make_score_result


class ExplainabilityLargeDatasetTests(unittest.TestCase):
    """Latency performance tests verifying execution budgets."""

    ITERATIONS: int = 1000

    def test_large_dataset_explainability_latency(self) -> None:
        """1000 sequential explain() invocations must execute within a 100ms budget."""
        engine = ExplainabilityEngine()
        sr = make_score_result()

        start = time.perf_counter()
        for _ in range(self.ITERATIONS):
            engine.explain(sr)
        duration_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(
            duration_ms,
            100.0,
            f"Explainability scale latency target exceeded: 1000 runs took {duration_ms:.2f} ms"
        )


if __name__ == "__main__":
    unittest.main()
