"""Unit tests for the SkillScoringRules DTO.

Purpose:
    Verify rules parameter defaults, Pydantic type checking, and DTO immutability.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules


class SkillScoringRulesTests(unittest.TestCase):
    """Test suite validating SkillScoringRules integrity."""

    def test_default_rules(self) -> None:
        rules = SkillScoringRules()
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)
        self.assertEqual(2.0, rules.mandatory_skill_weight)
        self.assertEqual(1.0, rules.optional_skill_weight)
        self.assertEqual(40.0, rules.maximum_skill_score)
        self.assertEqual(0.0, rules.minimum_skill_score)
        self.assertFalse(rules.allow_partial_matching)

    def test_rules_immutability(self) -> None:
        rules = SkillScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.mandatory_skill_weight = 5.0  # type: ignore

    def test_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            SkillScoringRules(extra_field="val")  # type: ignore
