"""Backward compatibility tests for ExperienceScoringRules.

Purpose:
    Protect the scoring contract by asserting that default rules parameters
    (weights, thresholds, score limits) are never silently changed.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules


class ExperienceRulesBackwardCompatibilityTests(unittest.TestCase):
    """Protects the API contract from silent drift in weights or ranges."""

    def test_verify_defaults_match_v1_contract(self) -> None:
        rules = ExperienceScoringRules()
        
        self.assertEqual(
            3.0,
            rules.exact_match_weight,
            "Backward compatibility check failed: exact_match_weight default has changed!"
        )
        self.assertEqual(
            1.5,
            rules.partial_match_weight,
            "Backward compatibility check failed: partial_match_weight default has changed!"
        )
        self.assertEqual(
            3.0,
            rules.overqualified_weight,
            "Backward compatibility check failed: overqualified_weight default has changed!"
        )
        self.assertEqual(
            0.5,
            rules.underqualified_weight,
            "Backward compatibility check failed: underqualified_weight default has changed!"
        )
        self.assertEqual(
            25.0,
            rules.maximum_experience_score,
            "Backward compatibility check failed: maximum_experience_score default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.minimum_experience_score,
            "Backward compatibility check failed: minimum_experience_score default has changed!"
        )
        self.assertEqual(
            True,
            rules.allow_partial_matching,
            "Backward compatibility check failed: allow_partial_matching default has changed!"
        )
        self.assertEqual(
            "STRICT",
            rules.strictness,
            "Backward compatibility check failed: strictness default has changed!"
        )
