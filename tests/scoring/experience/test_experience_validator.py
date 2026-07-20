"""Unit tests for the ExperienceScoreValidator.

Purpose:
    Verify duplicate match detection, matcher type checks, and metadata integrity.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.experience.validator import ExperienceScoreValidator
from ats_engine.domain.ats_scoring.experience.rules import ExperienceScoringRules
from ats_engine.domain.ats_scoring.exceptions import ExperienceValidationError
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result


class ExperienceScoreValidatorTests(unittest.TestCase):
    """Test suite validating ExperienceScoreValidator constraints."""

    def test_validator_rejects_duplicates(self) -> None:
        r1 = make_mock_exp_result("M-1", "R-1", "J-1")
        r2 = make_mock_exp_result("M-2", "R-1", "J-1")

        rules = ExperienceScoringRules()
        with self.assertRaises(ExperienceValidationError):
            ExperienceScoreValidator.validate([r1, r2], rules)

    def test_validator_rejects_null_metadata(self) -> None:
        r = make_mock_exp_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"metadata": None})  # type: ignore

        rules = ExperienceScoringRules()
        with self.assertRaises(ExperienceValidationError):
            ExperienceScoreValidator.validate([r], rules)

    def test_validator_rejects_unsupported_matcher_type(self) -> None:
        r = make_mock_exp_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"matcher_type": "SkillMatcher"})

        rules = ExperienceScoringRules()
        with self.assertRaises(ExperienceValidationError):
            ExperienceScoreValidator.validate([r], rules)

    def test_validator_rejects_unknown_classification(self) -> None:
        r = make_mock_exp_result("M-1", "R-1", "J-1", match_type="UNKNOWN_CLASSIFICATION")

        rules = ExperienceScoringRules()
        with self.assertRaises(ExperienceValidationError):
            ExperienceScoreValidator.validate([r], rules)
