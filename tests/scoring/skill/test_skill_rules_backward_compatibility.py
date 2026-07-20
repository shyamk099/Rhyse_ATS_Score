"""Backward compatibility tests for SkillScoringRules.

Purpose:
    Protect the scoring contract by asserting that default rules parameters
    (weights, thresholds, score limits) are never silently changed.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules


class SkillRulesBackwardCompatibilityTests(unittest.TestCase):
    """Protects the API contract from silent drift in weights or ranges."""

    def test_verify_defaults_match_v1_contract(self) -> None:
        rules = SkillScoringRules()
        
        # Verify strict adherence to Milestone 6.2 Pre-Implementation Specifications
        self.assertEqual(
            2.0,
            rules.mandatory_skill_weight,
            "Backward compatibility check failed: mandatory_skill_weight default has changed!"
        )
        self.assertEqual(
            1.0,
            rules.optional_skill_weight,
            "Backward compatibility check failed: optional_skill_weight default has changed!"
        )
        self.assertEqual(
            40.0,
            rules.maximum_skill_score,
            "Backward compatibility check failed: maximum_skill_score default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.minimum_skill_score,
            "Backward compatibility check failed: minimum_skill_score default has changed!"
        )
        self.assertEqual(
            False,
            rules.allow_partial_matching,
            "Backward compatibility check failed: allow_partial_matching default has changed!"
        )
        self.assertEqual(
            "STRICT",
            rules.strictness,
            "Backward compatibility check failed: strictness default has changed!"
        )
