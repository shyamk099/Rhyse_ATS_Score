"""Pipeline integration tests executing SkillScorer.

Purpose:
    Verify core ScoringPipeline execution utilizing registered SkillScorer,
    generating populated skill SectionScores while retaining placeholder results in other areas.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from tests.scoring.skill.test_skill_scorer import make_mock_result


class SkillPipelineTests(unittest.TestCase):
    """Test suite validating ScoringPipeline integration with SkillScorer."""

    def test_pipeline_integration_with_skill_scorer(self) -> None:
        registry = ScoringRegistry()
        registry.register("SKILL", SkillScorer, priority=100, enabled=True)

        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_result("M-1", "Python", "Python", is_mandatory=True),
            make_mock_result("M-2", "SQL", "SQL", is_mandatory=False),
        ]
        col = CanonicalMatchCollection(
            results=tuple(results),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )

        rules = ScoringRules()
        res = pipeline.execute(col, rules)

        self.assertIsNotNone(res)
        self.assertIsNone(res.overall_score)
        
        # Skill Score should be populated: 1 mandatory (2.0) + 1 optional (1.0) = 3.0
        self.assertIsNotNone(res.skill_score)
        self.assertEqual("SKILL", res.skill_score.section_name)
        self.assertEqual(3.0, res.skill_score.raw_score)
        self.assertEqual(40.0, res.skill_score.maximum_score)
        
        # Other scores remain placeholders
        self.assertIsNotNone(res.experience_score)
        self.assertIsNone(res.experience_score.raw_score)
        self.assertEqual("EXPERIENCE", res.experience_score.section_name)

        self.assertIsNotNone(res.education_score)
        self.assertIsNone(res.education_score.raw_score)
        self.assertEqual("EDUCATION", res.education_score.section_name)

        self.assertIsNotNone(res.project_score)
        self.assertIsNone(res.project_score.raw_score)
        self.assertEqual("PROJECT", res.project_score.section_name)

        self.assertIsNotNone(res.certification_score)
        self.assertIsNone(res.certification_score.raw_score)
        self.assertEqual("CERTIFICATION", res.certification_score.section_name)
