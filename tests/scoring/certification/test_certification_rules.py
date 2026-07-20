"""Unit tests for the CertificationScoringRules DTO.

Purpose:
    Verify rules parameter defaults, Pydantic type checking, and DTO immutability.
"""

from __future__ import annotations

import unittest
from pydantic import ValidationError

from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules


class CertificationScoringRulesTests(unittest.TestCase):
    """Test suite validating CertificationScoringRules integrity."""

    def test_default_rules(self) -> None:
        rules = CertificationScoringRules()
        self.assertEqual("1.0.0", rules.version)
        self.assertEqual("STRICT", rules.strictness)
        self.assertEqual(3.0, rules.exact_match_weight)
        self.assertEqual(2.5, rules.equivalent_certification_weight)
        self.assertEqual(2.0, rules.related_certification_weight)
        self.assertEqual(1.0, rules.partial_match_weight)
        self.assertEqual(0.5, rules.expired_certification_weight)
        self.assertEqual(10.0, rules.maximum_certification_score)
        self.assertEqual(0.0, rules.minimum_certification_score)
        self.assertTrue(rules.allow_related_certifications)
        self.assertTrue(rules.count_expired_certifications)

    def test_rules_immutability(self) -> None:
        rules = CertificationScoringRules()
        with self.assertRaises((ValidationError, TypeError)):
            rules.exact_match_weight = 5.0  # type: ignore

    def test_rules_forbid_extra(self) -> None:
        with self.assertRaises(ValidationError):
            CertificationScoringRules(extra_field="val")  # type: ignore
