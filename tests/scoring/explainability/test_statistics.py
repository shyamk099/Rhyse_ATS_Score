"""Tests for ExplainabilityStatisticsBuilder.

Purpose:
    Verify statistics dictionary contains execution timing and outcome metrics.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.explainability.statistics_builder import ExplainabilityStatisticsBuilder


class ExplainabilityStatisticsTests(unittest.TestCase):
    """Test suite validating explainability statistics builder."""

    def test_statistics_fields(self) -> None:
        """Verify built stats dict contains all required telemetry metrics."""
        stats = ExplainabilityStatisticsBuilder.build(
            execution_time_ms=12.34567,
            sections_processed=("SKILL", "EXPERIENCE"),
            formula_generation_time_ms=4.56,
            formatting_time_ms=7.78,
            success=True,
        )
        self.assertEqual(12.3457, stats["execution_time_ms"])
        self.assertEqual(("SKILL", "EXPERIENCE"), stats["sections_processed"])
        self.assertEqual(4.56, stats["formula_generation_time_ms"])
        self.assertEqual(7.78, stats["formatting_time_ms"])
        self.assertTrue(stats["success"])


if __name__ == "__main__":
    unittest.main()
