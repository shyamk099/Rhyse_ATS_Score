"""Unit tests for the ProjectScoringRules DTO.

Purpose:
    Verify rules parameter defaults, Pydantic type checking, and DTO immutability.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules


class ProjectScoringRulesTests(unittest.TestCase):
    """Test suite validating ProjectScoringRules integrity."""

    def test_default_rules(self) -> None:
        rules = ProjectScoringRules()
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)
        self.assertEqual(3.0, rules.exact_match_weight)
        self.assertEqual(2.5, rules.similar_project_weight)
        self.assertEqual(2.0, rules.related_project_weight)
        self.assertEqual(1.0, rules.partial_match_weight)
        self.assertEqual(15.0, rules.maximum_project_score)
        self.assertEqual(0.0, rules.minimum_project_score)
        self.assertTrue(rules.allow_related_projects)

    def test_rules_immutability(self) -> None:
        rules = ProjectScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.exact_match_weight = 5.0  # type: ignore

    def test_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            ProjectScoringRules(extra_field="val")  # type: ignore
