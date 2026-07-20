"""Unit tests for the ProjectScoreValidator.

Purpose:
    Verify duplicate match detection, matcher type checks, and metadata integrity.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.project.validator import ProjectScoreValidator
from ats_engine.domain.ats_scoring.project.rules import ProjectScoringRules
from ats_engine.domain.ats_scoring.exceptions import ProjectValidationError
from tests.scoring.project.test_project_scorer import make_mock_proj_result


class ProjectScoreValidatorTests(unittest.TestCase):
    """Test suite validating ProjectScoreValidator constraints."""

    def test_validator_rejects_duplicates(self) -> None:
        r1 = make_mock_proj_result("M-1", "R-1", "J-1")
        r2 = make_mock_proj_result("M-2", "R-1", "J-1")

        rules = ProjectScoringRules()
        with self.assertRaises(ProjectValidationError):
            ProjectScoreValidator.validate([r1, r2], rules)

    def test_validator_rejects_null_metadata(self) -> None:
        r = make_mock_proj_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"metadata": None})  # type: ignore

        rules = ProjectScoringRules()
        with self.assertRaises(ProjectValidationError):
            ProjectScoreValidator.validate([r], rules)

    def test_validator_rejects_unsupported_matcher_type(self) -> None:
        r = make_mock_proj_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"matcher_type": "SkillMatcher"})

        rules = ProjectScoringRules()
        with self.assertRaises(ProjectValidationError):
            ProjectScoreValidator.validate([r], rules)

    def test_validator_rejects_unknown_classification(self) -> None:
        r = make_mock_proj_result("M-1", "R-1", "J-1", match_type="UNKNOWN_CLASSIFICATION")

        rules = ProjectScoringRules()
        with self.assertRaises(ProjectValidationError):
            ProjectScoreValidator.validate([r], rules)
