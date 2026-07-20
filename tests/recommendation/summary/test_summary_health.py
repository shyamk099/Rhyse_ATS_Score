"""Tests for ResumeHealthPolicy.

Purpose:
    Verify deterministic health classification from high-priority counts.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.summary.policy import ResumeHealthPolicy
from ats_engine.domain.recommendation.summary.models import ResumeHealth


class HealthPolicyTests(unittest.TestCase):
    """Test suite validating ResumeHealthPolicy deterministic mappings."""

    def test_zero_high_excellent(self) -> None:
        """0 high priority must yield Excellent."""
        health = ResumeHealthPolicy.evaluate(0)
        self.assertIsInstance(health, ResumeHealth)
        self.assertEqual(100.0, health.score)
        self.assertEqual("A", health.grade)
        self.assertEqual("Excellent", health.status)

    def test_one_high_good(self) -> None:
        """1 high priority must yield Good."""
        health = ResumeHealthPolicy.evaluate(1)
        self.assertEqual(85.0, health.score)
        self.assertEqual("B", health.grade)
        self.assertEqual("Good", health.status)

    def test_two_high_good(self) -> None:
        """2 high priority must yield Good."""
        health = ResumeHealthPolicy.evaluate(2)
        self.assertEqual(85.0, health.score)
        self.assertEqual("B", health.grade)

    def test_three_high_needs_improvement(self) -> None:
        """3 high priority must yield Needs Improvement."""
        health = ResumeHealthPolicy.evaluate(3)
        self.assertEqual(70.0, health.score)
        self.assertEqual("C", health.grade)
        self.assertEqual("Needs Improvement", health.status)

    def test_five_high_needs_improvement(self) -> None:
        """5 high priority must yield Needs Improvement."""
        health = ResumeHealthPolicy.evaluate(5)
        self.assertEqual(70.0, health.score)
        self.assertEqual("C", health.grade)

    def test_six_high_critical(self) -> None:
        """6 high priority must yield Critical."""
        health = ResumeHealthPolicy.evaluate(6)
        self.assertEqual(50.0, health.score)
        self.assertEqual("D", health.grade)
        self.assertEqual("Critical", health.status)

    def test_large_high_critical(self) -> None:
        """100 high priority must yield Critical."""
        health = ResumeHealthPolicy.evaluate(100)
        self.assertEqual(50.0, health.score)
        self.assertEqual("D", health.grade)

    def test_negative_raises_value_error(self) -> None:
        """Negative count must raise ValueError."""
        with self.assertRaises(ValueError):
            ResumeHealthPolicy.evaluate(-1)

    def test_immutability(self) -> None:
        """ResumeHealth DTO must be immutable."""
        health = ResumeHealthPolicy.evaluate(0)
        with self.assertRaises(Exception):
            health.score = 50.0  # type: ignore[misc]

    def test_boundary_two_to_three(self) -> None:
        """Boundary between Good (2) and Needs Improvement (3) must be exact."""
        h2 = ResumeHealthPolicy.evaluate(2)
        h3 = ResumeHealthPolicy.evaluate(3)
        self.assertEqual("B", h2.grade)
        self.assertEqual("C", h3.grade)

    def test_boundary_five_to_six(self) -> None:
        """Boundary between Needs Improvement (5) and Critical (6) must be exact."""
        h5 = ResumeHealthPolicy.evaluate(5)
        h6 = ResumeHealthPolicy.evaluate(6)
        self.assertEqual("C", h5.grade)
        self.assertEqual("D", h6.grade)


if __name__ == "__main__":
    unittest.main()
