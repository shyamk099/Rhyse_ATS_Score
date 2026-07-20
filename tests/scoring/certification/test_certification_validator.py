"""Unit tests for the CertificationScoreValidator.

Purpose:
    Verify duplicate match detection, matcher type checks, and metadata integrity.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.certification.validator import CertificationScoreValidator
from ats_engine.domain.ats_scoring.certification.rules import CertificationScoringRules
from ats_engine.domain.ats_scoring.exceptions import CertificationValidationError
from tests.scoring.certification.test_certification_scorer import make_mock_cert_result


class CertificationScoreValidatorTests(unittest.TestCase):
    """Test suite validating CertificationScoreValidator constraints."""

    def test_validator_rejects_duplicates(self) -> None:
        r1 = make_mock_cert_result("M-1", "R-1", "J-1")
        r2 = make_mock_cert_result("M-2", "R-1", "J-1")

        rules = CertificationScoringRules()
        with self.assertRaises(CertificationValidationError):
            CertificationScoreValidator.validate([r1, r2], rules)

    def test_validator_rejects_null_metadata(self) -> None:
        r = make_mock_cert_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"metadata": None})  # type: ignore

        rules = CertificationScoringRules()
        with self.assertRaises(CertificationValidationError):
            CertificationScoreValidator.validate([r], rules)

    def test_validator_rejects_unsupported_matcher_type(self) -> None:
        r = make_mock_cert_result("M-1", "R-1", "J-1")
        r = r.model_copy(update={"matcher_type": "SkillMatcher"})

        rules = CertificationScoringRules()
        with self.assertRaises(CertificationValidationError):
            CertificationScoreValidator.validate([r], rules)

    def test_validator_rejects_unknown_classification(self) -> None:
        r = make_mock_cert_result("M-1", "R-1", "J-1", match_type="UNKNOWN_CLASSIFICATION")

        rules = CertificationScoringRules()
        with self.assertRaises(CertificationValidationError):
            CertificationScoreValidator.validate([r], rules)
