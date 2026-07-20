"""Unit tests for the ScoreValidator.

Purpose:
    Verify validations on Nulls, version mappings, supported category keys, and read-only attributes.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.common.validator import ScoreValidator
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.exceptions import ScoringValidationError


class MockMatchResult:
    def __init__(self, matcher_type: str) -> None:
        self.matcher_type = matcher_type


class ScoreValidatorTests(unittest.TestCase):
    """Test suite validating ScoreValidator constraints."""

    def test_validator_rejects_none_match_collection(self) -> None:
        rules = ScoringRules()
        with self.assertRaises(ScoringValidationError):
            ScoreValidator.validate(None, rules)  # type: ignore

    def test_validator_accepts_valid_collection(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()
        # Should not raise exception
        ScoreValidator.validate(col, rules)

    def test_validator_rejects_incompatible_rules_version(self) -> None:
        col = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules(version="2.0.0")
        with self.assertRaises(ScoringValidationError):
            ScoreValidator.validate(col, rules)

    def test_validator_rejects_unsupported_matcher_category(self) -> None:
        bad_result = MockMatchResult(matcher_type="UnsupportedMatcher")
        col = CanonicalMatchCollection(
            results=(bad_result,),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()
        with self.assertRaises(ScoringValidationError):
            ScoreValidator.validate(col, rules)

    def test_validator_accepts_supported_matcher_categories(self) -> None:
        r1 = MockMatchResult(matcher_type="SkillMatcher")
        r2 = MockMatchResult(matcher_type="ExperienceMatcher")
        col = CanonicalMatchCollection(
            results=(r1, r2),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()
        # Should not raise exception
        ScoreValidator.validate(col, rules)
