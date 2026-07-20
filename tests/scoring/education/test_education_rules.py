"""Unit tests for the EducationScoringRules DTO.

Purpose:
    Verify rules parameter defaults, Pydantic type checking, and DTO immutability.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules


class EducationScoringRulesTests(unittest.TestCase):
    """Test suite validating EducationScoringRules integrity."""

    def test_default_rules(self) -> None:
        rules = EducationScoringRules()
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)
        self.assertEqual(4.0, rules.exact_match_weight)
        self.assertEqual(4.0, rules.higher_than_required_weight)
        self.assertEqual(2.5, rules.related_field_weight)
        self.assertEqual(1.0, rules.lower_than_required_weight)
        self.assertEqual(0.0, rules.unrelated_field_weight)
        self.assertEqual(15.0, rules.maximum_education_score)
        self.assertEqual(0.0, rules.minimum_education_score)
        self.assertTrue(rules.allow_related_fields)

    def test_rules_immutability(self) -> None:
        rules = EducationScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.exact_match_weight = 5.0  # type: ignore

    def test_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            EducationScoringRules(extra_field="val")  # type: ignore
