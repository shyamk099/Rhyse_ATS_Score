"""Backward compatibility tests for CertificationScoringRules.

Purpose:
    Protect the scoring contract by asserting that default rules parameters
    (weights, thresholds, score limits) are never silently changed.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules


class CertificationRulesBackwardCompatibilityTests(unittest.TestCase):
    """Protects the API contract from silent drift in weights or ranges."""

    def test_verify_defaults_match_v1_contract(self) -> None:
        rules = CertificationScoringRules()
        
        self.assertEqual(
            3.0,
            rules.exact_match_weight,
            "Backward compatibility check failed: exact_match_weight default has changed!"
        )
        self.assertEqual(
            2.5,
            rules.equivalent_certification_weight,
            "Backward compatibility check failed: equivalent_certification_weight default has changed!"
        )
        self.assertEqual(
            2.0,
            rules.related_certification_weight,
            "Backward compatibility check failed: related_certification_weight default has changed!"
        )
        self.assertEqual(
            1.0,
            rules.partial_match_weight,
            "Backward compatibility check failed: partial_match_weight default has changed!"
        )
        self.assertEqual(
            0.5,
            rules.expired_certification_weight,
            "Backward compatibility check failed: expired_certification_weight default has changed!"
        )
        self.assertEqual(
            10.0,
            rules.maximum_certification_score,
            "Backward compatibility check failed: maximum_certification_score default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.minimum_certification_score,
            "Backward compatibility check failed: minimum_certification_score default has changed!"
        )
        self.assertEqual(
            True,
            rules.allow_related_certifications,
            "Backward compatibility check failed: allow_related_certifications default has changed!"
        )
        self.assertEqual(
            True,
            rules.count_expired_certifications,
            "Backward compatibility check failed: count_expired_certifications default has changed!"
        )
        self.assertEqual(
            "STRICT",
            rules.strictness,
            "Backward compatibility check failed: strictness default has changed!"
        )
