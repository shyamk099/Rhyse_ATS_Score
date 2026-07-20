"""Unit tests for the ExperienceScoringRules DTO.

Purpose:
    Verify rules parameter defaults, Pydantic type checking, and DTO immutability.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules


class ExperienceScoringRulesTests(unittest.TestCase):
    """Test suite validating ExperienceScoringRules integrity."""

    def test_default_rules(self) -> None:
        rules = ExperienceScoringRules()
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)
        self.assertEqual(3.0, rules.exact_match_weight)
        self.assertEqual(1.5, rules.partial_match_weight)
        self.assertEqual(3.0, rules.overqualified_weight)
        self.assertEqual(0.5, rules.underqualified_weight)
        self.assertEqual(25.0, rules.maximum_experience_score)
        self.assertEqual(0.0, rules.minimum_experience_score)
        self.assertTrue(rules.allow_partial_matching)

    def test_rules_immutability(self) -> None:
        rules = ExperienceScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.exact_match_weight = 5.0  # type: ignore

    def test_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            ExperienceScoringRules(extra_field="val")  # type: ignore
