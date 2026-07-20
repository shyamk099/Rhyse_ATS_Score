"""Tests for OrchestratorStatisticsBuilder.

Purpose:
    Verify the statistics builder produces correct keys, value types,
    and handles edge cases like empty inputs and zero latency.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.orchestrator.statistics_builder import OrchestratorStatisticsBuilder


class OrchestratorStatisticsBuilderTests(unittest.TestCase):
    """Tests for OrchestratorStatisticsBuilder.build()."""

    def test_returns_dict(self) -> None:
        """build() must return a plain dict."""
        result = OrchestratorStatisticsBuilder.build()
        self.assertIsInstance(result, dict)

    def test_required_keys_present(self) -> None:
        """All required keys must be present in the output."""
        result = OrchestratorStatisticsBuilder.build()
        expected_keys = {
            "execution_time_ms",
            "section_execution_times",
            "sections_executed",
            "sections_skipped",
            "failed_sections",
            "pipeline_version",
            "success",
        }
        self.assertEqual(expected_keys, set(result.keys()))

    def test_default_values(self) -> None:
        """Default build must produce sensible zero-state values."""
        result = OrchestratorStatisticsBuilder.build()
        self.assertEqual(0.0, result["execution_time_ms"])
        self.assertEqual({}, result["section_execution_times"])
        self.assertEqual((), result["sections_executed"])
        self.assertEqual((), result["sections_skipped"])
        self.assertEqual((), result["failed_sections"])
        self.assertEqual("1.0.0", result["pipeline_version"])
        self.assertTrue(result["success"])

    def test_execution_time_is_rounded(self) -> None:
        """execution_time_ms must be rounded to 4 decimal places."""
        result = OrchestratorStatisticsBuilder.build(execution_time_ms=12.123456789)
        self.assertEqual(round(12.123456789, 4), result["execution_time_ms"])

    def test_sections_executed_stored_as_tuple(self) -> None:
        """sections_executed must be stored as a tuple."""
        result = OrchestratorStatisticsBuilder.build(
            sections_executed=("SKILL", "EXPERIENCE")
        )
        self.assertIsInstance(result["sections_executed"], tuple)
        self.assertIn("SKILL", result["sections_executed"])

    def test_sections_skipped_stored_as_tuple(self) -> None:
        """sections_skipped must be stored as a tuple."""
        result = OrchestratorStatisticsBuilder.build(sections_skipped=("EDUCATION",))
        self.assertIsInstance(result["sections_skipped"], tuple)
        self.assertIn("EDUCATION", result["sections_skipped"])

    def test_failed_sections_stored_as_tuple(self) -> None:
        """failed_sections must be stored as a tuple."""
        result = OrchestratorStatisticsBuilder.build(failed_sections=("PROJECT",))
        self.assertIsInstance(result["failed_sections"], tuple)
        self.assertIn("PROJECT", result["failed_sections"])

    def test_section_execution_times_is_dict_copy(self) -> None:
        """section_execution_times must be a copy of the input dict."""
        times = {"SKILL": 5.0, "EXPERIENCE": 3.0}
        result = OrchestratorStatisticsBuilder.build(section_execution_times=times)
        self.assertEqual(times, result["section_execution_times"])
        # Must be a copy, not the same object
        result["section_execution_times"]["SKILL"] = 999.0
        self.assertEqual(5.0, times["SKILL"])

    def test_success_false_propagated(self) -> None:
        """success=False must be stored correctly."""
        result = OrchestratorStatisticsBuilder.build(success=False)
        self.assertFalse(result["success"])

    def test_pipeline_version_stored(self) -> None:
        """Custom pipeline_version must be stored."""
        result = OrchestratorStatisticsBuilder.build(pipeline_version="2.5.0")
        self.assertEqual("2.5.0", result["pipeline_version"])

    def test_none_section_times_defaults_to_empty_dict(self) -> None:
        """None section_execution_times must be treated as an empty dict."""
        result = OrchestratorStatisticsBuilder.build(section_execution_times=None)
        self.assertEqual({}, result["section_execution_times"])


if __name__ == "__main__":
    unittest.main()
