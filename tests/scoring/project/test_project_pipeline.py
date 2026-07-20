"""Pipeline integration tests executing ProjectScorer.

Purpose:
    Verify core ScoringPipeline execution utilizing registered ProjectScorer,
    generating populated project SectionScores in sequential pipeline flow.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
from ats_engine.domain.ats_scoring.education.scorer import EducationScorer
from ats_engine.domain.ats_scoring.project.scorer import ProjectScorer
from tests.scoring.skill.test_skill_scorer import make_mock_result
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result
from tests.scoring.education.test_education_scorer import make_mock_edu_result
from tests.scoring.project.test_project_scorer import make_mock_proj_result


class ProjectPipelineTests(unittest.TestCase):
    """Test suite validating ScoringPipeline integration with ProjectScorer."""

    def test_pipeline_integration_with_project_scorer(self) -> None:
        registry = ScoringRegistry()
        registry.register("SKILL", SkillScorer, priority=100, enabled=True)
        registry.register("EXPERIENCE", ExperienceScorer, priority=200, enabled=True)
        registry.register("EDUCATION", EducationScorer, priority=300, enabled=True)
        registry.register("PROJECT", ProjectScorer, priority=400, enabled=True)

        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_result("M-S1", "Python", "Python", is_mandatory=True),
            make_mock_exp_result("M-E1", "Manager", "Manager", match_type="EXACT_MATCH"),
            make_mock_edu_result("M-ED1", "BSc", "BSc", match_type="EXACT_MATCH"),
            make_mock_proj_result("M-P1", "Scoring Engine", "Scoring Engine", match_type="EXACT_MATCH"),
            make_mock_proj_result("M-P2", "Parser Engine", "Parser Engine", match_type="SIMILAR_PROJECT"),
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
        
        # Skill Score should be populated: 1 mandatory (2.0) = 2.0
        self.assertIsNotNone(res.skill_score)
        self.assertEqual("SKILL", res.skill_score.section_name)
        self.assertEqual(2.0, res.skill_score.raw_score)
        
        # Experience Score should be populated: 1 exact (3.0) = 3.0
        self.assertIsNotNone(res.experience_score)
        self.assertEqual("EXPERIENCE", res.experience_score.section_name)
        self.assertEqual(3.0, res.experience_score.raw_score)

        # Education Score should be populated: 1 exact (4.0) = 4.0
        self.assertIsNotNone(res.education_score)
        self.assertEqual("EDUCATION", res.education_score.section_name)
        self.assertEqual(4.0, res.education_score.raw_score)

        # Project Score should be populated: 1 exact (3.0) + 1 similar (2.5) = 5.5
        self.assertIsNotNone(res.project_score)
        self.assertEqual("PROJECT", res.project_score.section_name)
        self.assertEqual(5.5, res.project_score.raw_score)
        self.assertEqual(15.0, res.project_score.maximum_score)
        
        # Remaining scores are placeholders
        self.assertIsNotNone(res.certification_score)
        self.assertIsNone(res.certification_score.raw_score)
