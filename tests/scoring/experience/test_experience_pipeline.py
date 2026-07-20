"""Pipeline integration tests executing ExperienceScorer.

Purpose:
    Verify core ScoringPipeline execution utilizing registered ExperienceScorer,
    generating populated experience SectionScores in sequential pipeline flow.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
from tests.scoring.skill.test_skill_scorer import make_mock_result
from tests.scoring.experience.test_experience_scorer import make_mock_exp_result


class ExperiencePipelineTests(unittest.TestCase):
    """Test suite validating ScoringPipeline integration with ExperienceScorer."""

    def test_pipeline_integration_with_experience_scorer(self) -> None:
        registry = ScoringRegistry()
        registry.register("SKILL", SkillScorer, priority=100, enabled=True)
        registry.register("EXPERIENCE", ExperienceScorer, priority=200, enabled=True)

        pipeline = ScoringPipeline(registry=registry)

        results = [
            make_mock_result("M-S1", "Python", "Python", is_mandatory=True),
            make_mock_exp_result("M-E1", "Manager", "Manager", match_type="EXACT_MATCH"),
            make_mock_exp_result("M-E2", "Developer", "Developer", match_type="PARTIAL_MATCH"),
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
        
        # Experience Score should be populated: 1 exact (3.0) + 1 partial (1.5) = 4.5
        self.assertIsNotNone(res.experience_score)
        self.assertEqual("EXPERIENCE", res.experience_score.section_name)
        self.assertEqual(4.5, res.experience_score.raw_score)
        self.assertEqual(25.0, res.experience_score.maximum_score)
        
        # Other scores remain placeholders
        self.assertIsNotNone(res.education_score)
        self.assertIsNone(res.education_score.raw_score)
