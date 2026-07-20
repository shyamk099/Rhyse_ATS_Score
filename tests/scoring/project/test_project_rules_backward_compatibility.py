"""Backward compatibility tests for ProjectScoringRules.

Purpose:
    Protect the scoring contract by asserting that default rules parameters
    (weights, thresholds, score limits) are never silently changed.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules


class ProjectRulesBackwardCompatibilityTests(unittest.TestCase):
    """Protects the API contract from silent drift in weights or ranges."""

    def test_verify_defaults_match_v1_contract(self) -> None:
        rules = ProjectScoringRules()
        
        self.assertEqual(
            3.0,
            rules.exact_match_weight,
            "Backward compatibility check failed: exact_match_weight default has changed!"
        )
        self.assertEqual(
            2.5,
            rules.similar_project_weight,
            "Backward compatibility check failed: similar_project_weight default has changed!"
        )
        self.assertEqual(
            2.0,
            rules.related_project_weight,
            "Backward compatibility check failed: related_project_weight default has changed!"
        )
        self.assertEqual(
            1.0,
            rules.partial_match_weight,
            "Backward compatibility check failed: partial_match_weight default has changed!"
        )
        self.assertEqual(
            15.0,
            rules.maximum_project_score,
            "Backward compatibility check failed: maximum_project_score default has changed!"
        )
        self.assertEqual(
            0.0,
            rules.minimum_project_score,
            "Backward compatibility check failed: minimum_project_score default has changed!"
        )
        self.assertEqual(
            True,
            rules.allow_related_projects,
            "Backward compatibility check failed: allow_related_projects default has changed!"
        )
        self.assertEqual(
            "STRICT",
            rules.strictness,
            "Backward compatibility check failed: strictness default has changed!"
        )
