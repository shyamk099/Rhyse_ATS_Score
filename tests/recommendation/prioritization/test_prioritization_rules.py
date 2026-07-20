"""Tests for PrioritizationRules.

Purpose:
    Verify prioritization rules maps key mapping profiles correctly.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.prioritization.prioritization_rules import PrioritizationRules


class PrioritizationRulesTests(unittest.TestCase):
    """Test suite validating PrioritizationRules configuration mapping."""

    def setUp(self) -> None:
        self.rules = PrioritizationRules()

    def test_resolve_default_profiles(self) -> None:
        """Rules must resolve matching priority, impact, and confidence values for standard categories."""
        skill_missing = self.rules.resolve_profile("skill", "SKILL_MISSING")
        self.assertEqual(100, skill_missing.priority)
        self.assertEqual(1.0, skill_missing.impact)
        self.assertEqual(1.0, skill_missing.confidence)

        proj_missing = self.rules.resolve_profile("project", "PROJECT_MISSING")
        self.assertEqual(80, proj_missing.priority)
        self.assertEqual(0.75, proj_missing.impact)
        self.assertEqual(1.0, proj_missing.confidence)

        cert_expired = self.rules.resolve_profile("certification", "CERTIFICATION_EXPIRED")
        self.assertEqual(85, cert_expired.priority)
        self.assertEqual(0.90, cert_expired.impact)
        self.assertEqual(0.95, cert_expired.confidence)

    def test_resolve_fallback_profile(self) -> None:
        """Resolving an unknown category/section must yield a safe default fallback profile."""
        fallback = self.rules.resolve_profile("unknown_section", "UNKNOWN_CATEGORY")
        self.assertEqual(50, fallback.priority)
        self.assertEqual(0.50, fallback.impact)
        self.assertEqual(0.90, fallback.confidence)

    def test_priority_thresholds(self) -> None:
        """Rules must correctly categorize priority values into high, medium, or low classifications."""
        self.assertTrue(self.rules.is_high(100))
        self.assertTrue(self.rules.is_high(85))
        self.assertFalse(self.rules.is_high(80))

        self.assertTrue(self.rules.is_medium(80))
        self.assertTrue(self.rules.is_medium(70))
        self.assertFalse(self.rules.is_medium(65))

        self.assertTrue(self.rules.is_low(65))
        self.assertTrue(self.rules.is_low(0))


if __name__ == "__main__":
    unittest.main()
