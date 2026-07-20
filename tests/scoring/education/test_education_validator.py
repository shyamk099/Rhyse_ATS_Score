"""Unit tests for the EducationScoreValidator.

Purpose:
    Verify duplicate match detection, matcher type checks, and metadata integrity.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.education.validator import EducationScoreValidator
from ats_engine.domain.ats_scoring.education.rules import EducationScoringRules
from ats_engine.domain.ats_scoring.exceptions import EducationValidationError
from tests.scoring.education.test_education_scorer import make_mock_edu_result


class EducationScoreValidatorTests(unittest.TestCase):
    """Test suite validating EducationScoreValidator constraints."""

    def test_validator_rejects_duplicates(self) -> None:
        r1 = make_mock_edu_result("M-1", "R-1", "J-1")
        r2 = make_mock_edu_result("M-2", "R-1", "J-1")

        rules = EducationScoringRules()
        with self.assertRaises(EducationValidationError):
            EducationScoreValidator.validate([r1, r2], rules)

    def test_validator_rejects_null_metadata(self) -> None:
        r = make_mock_edu_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"metadata": None})  # type: ignore

        rules = EducationScoringRules()
        with self.assertRaises(EducationValidationError):
            EducationScoreValidator.validate([r], rules)

    def test_validator_rejects_unsupported_matcher_type(self) -> None:
        r = make_mock_edu_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"matcher_type": "SkillMatcher"})

        rules = EducationScoringRules()
        with self.assertRaises(EducationValidationError):
            EducationScoreValidator.validate([r], rules)

    def test_validator_rejects_unknown_classification(self) -> None:
        r = make_mock_edu_result("M-1", "R-1", "J-1", match_type="UNKNOWN_CLASSIFICATION")

        rules = EducationScoringRules()
        with self.assertRaises(EducationValidationError):
            EducationScoreValidator.validate([r], rules)
