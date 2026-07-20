"""Unit tests for the SkillScoreValidator.

Purpose:
    Verify duplicate match detection, matcher type check, and null metadata validation rejections.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.skill.validator import SkillScoreValidator
from ats_engine.domain.ats_scoring.skill.rules import SkillScoringRules
from ats_engine.domain.ats_scoring.exceptions import SkillValidationError
from tests.scoring.skill.test_skill_scorer import make_mock_result


class SkillScoreValidatorTests(unittest.TestCase):
    """Test suite validating SkillScoreValidator constraints."""

    def test_validator_rejects_duplicates(self) -> None:
        r1 = make_mock_result("M-1", "R-1", "J-1")
        r2 = make_mock_result("M-2", "R-1", "J-1")  # duplicate resume/job pair

        rules = SkillScoringRules()
        with self.assertRaises(SkillValidationError):
            SkillScoreValidator.validate([r1, r2], rules)

    def test_validator_rejects_null_metadata(self) -> None:
        r = make_mock_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"metadata": None})  # type: ignore

        rules = SkillScoringRules()
        with self.assertRaises(SkillValidationError):
            SkillScoreValidator.validate([r], rules)

    def test_validator_rejects_unsupported_matcher_type(self) -> None:
        r = make_mock_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"matcher_type": "ExpMatcher"})

        rules = SkillScoringRules()
        with self.assertRaises(SkillValidationError):
            SkillScoreValidator.validate([r], rules)
