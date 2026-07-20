"""Tests for AggregationValidator.

Purpose:
    Verify pre-aggregation validation catches None result, missing sections,
    None raw_score, zero maximum_score, and invalid weights.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.validator import AggregationValidator
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.exceptions import AggregationValidationError

from tests.scoring.aggregation.helpers import (
    make_score_result,
    make_section,
    make_metadata,
    make_statistics,
    make_default_weights,
)


class AggregationValidatorTests(unittest.TestCase):
    """Tests for AggregationValidator.validate()."""

    def _make_result_without(self, field: str) -> ScoreResult:
        """Build a ScoreResult with one section set to None."""
        all_sections = {
            "skill_score": make_section("SKILL", 10.0, 20.0),
            "experience_score": make_section("EXPERIENCE", 15.0, 25.0),
            "education_score": make_section("EDUCATION", 9.0, 15.0),
            "project_score": make_section("PROJECT", 8.0, 15.0),
            "certification_score": make_section("CERTIFICATION", 6.0, 10.0),
        }
        all_sections[field] = None
        return ScoreResult(
            **all_sections,
            statistics=make_statistics(),
            metadata=make_metadata(),
        )

    def test_valid_result_passes(self) -> None:
        """A fully valid ScoreResult must pass without exception."""
        AggregationValidator.validate(make_score_result(), make_default_weights())

    def test_missing_skill_raises(self) -> None:
        """Missing skill_score must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError) as ctx:
            AggregationValidator.validate(
                self._make_result_without("skill_score"), make_default_weights()
            )
        self.assertIn("SKILL", str(ctx.exception))

    def test_missing_experience_raises(self) -> None:
        """Missing experience_score must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError) as ctx:
            AggregationValidator.validate(
                self._make_result_without("experience_score"), make_default_weights()
            )
        self.assertIn("EXPERIENCE", str(ctx.exception))

    def test_missing_education_raises(self) -> None:
        """Missing education_score must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(
                self._make_result_without("education_score"), make_default_weights()
            )

    def test_missing_project_raises(self) -> None:
        """Missing project_score must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(
                self._make_result_without("project_score"), make_default_weights()
            )

    def test_missing_certification_raises(self) -> None:
        """Missing certification_score must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(
                self._make_result_without("certification_score"), make_default_weights()
            )

    def test_none_raw_score_raises(self) -> None:
        """A section with None raw_score must raise AggregationValidationError."""
        result = ScoreResult(
            skill_score=SectionScore(section_name="SKILL", raw_score=None, maximum_score=40.0),
            experience_score=make_section("EXPERIENCE", 15.0, 25.0),
            education_score=make_section("EDUCATION", 9.0, 15.0),
            project_score=make_section("PROJECT", 8.0, 15.0),
            certification_score=make_section("CERTIFICATION", 6.0, 10.0),
            statistics=make_statistics(),
            metadata=make_metadata(),
        )
        with self.assertRaises(AggregationValidationError) as ctx:
            AggregationValidator.validate(result, make_default_weights())
        self.assertIn("SKILL", str(ctx.exception))

    def test_zero_maximum_score_raises(self) -> None:
        """A section with maximum_score == 0 must raise AggregationValidationError."""
        result = ScoreResult(
            skill_score=SectionScore(section_name="SKILL", raw_score=10.0, maximum_score=0.0),
            experience_score=make_section("EXPERIENCE", 15.0, 25.0),
            education_score=make_section("EDUCATION", 9.0, 15.0),
            project_score=make_section("PROJECT", 8.0, 15.0),
            certification_score=make_section("CERTIFICATION", 6.0, 10.0),
            statistics=make_statistics(),
            metadata=make_metadata(),
        )
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(result, make_default_weights())

    def test_none_maximum_score_raises(self) -> None:
        """A section with maximum_score == None must raise AggregationValidationError."""
        result = ScoreResult(
            skill_score=SectionScore(section_name="SKILL", raw_score=10.0, maximum_score=None),
            experience_score=make_section("EXPERIENCE", 15.0, 25.0),
            education_score=make_section("EDUCATION", 9.0, 15.0),
            project_score=make_section("PROJECT", 8.0, 15.0),
            certification_score=make_section("CERTIFICATION", 6.0, 10.0),
            statistics=make_statistics(),
            metadata=make_metadata(),
        )
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(result, make_default_weights())

    def test_none_weight_config_raises(self) -> None:
        """None weight_config must raise AggregationValidationError."""
        with self.assertRaises(AggregationValidationError):
            AggregationValidator.validate(make_score_result(), None)  # type: ignore[arg-type]

    def test_all_five_sections_with_valid_scores_passes(self) -> None:
        """Five valid sections must all pass the validator without exception."""
        AggregationValidator.validate(make_score_result(), make_default_weights())


if __name__ == "__main__":
    unittest.main()
