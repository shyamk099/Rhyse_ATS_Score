"""Backward compatibility tests for EducationScoringRules.

Purpose:
    Protect the scoring contract by asserting that default rules parameters
    (weights, thresholds, score limits) are never silently changed.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules


class EducationRulesBackwardCompatibilityTests(unittest.TestCase):
    """Protects the API contract from silent drift in weights or ranges."""

    def test_verify_defaults_match_v1_contract(self) -> None:
        rules = EducationScoringRules()
        
        self.assertEqual(
            4.0,
            rules.exact_match_weight,
            "Backward compatibility check failed: exact_match_weight default has changed!"
        )
        self.assertEqual(
            4.0,
            rules.higher_than_required_weight,
            "Backward compatibility check failed: higher_than_required_weight default has changed!"
        )
        self.assertEqual(
            2.5,
            rules.related_field_weight,
            "Backward compatibility check failed: related_field_weight default has changed!"
        )
        self.assertEqual(
            1.0,
            rules.lower_than_required_weight,
            "Backward compatibility check failed: lower_than_required_weight default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.unrelated_field_weight,
            "Backward compatibility check failed: unrelated_field_weight default has changed!"
        )
        self.assertEqual(
            15.0,
            rules.maximum_education_score,
            "Backward compatibility check failed: maximum_education_score default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.minimum_education_score,
            "Backward compatibility check failed: minimum_education_score default has changed!"
        )
        self.assertEqual(
            True,
            rules.allow_related_fields,
            "Backward compatibility check failed: allow_related_fields default has changed!"
        )
        self.assertEqual(
            "STRICT",
            rules.strictness,
            "Backward compatibility check failed: strictness default has changed!"
        )
