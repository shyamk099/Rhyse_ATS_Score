"""RecommendationFactory definition.

Purpose:
    Provide static factory methods for constructing fully wired
    RecommendationEngine instances.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry


class RecommendationFactory:
    """Factory for constructing RecommendationEngine instances.

    At Milestone 7.1 (framework-only), the default engine has an empty registry
    with no providers registered. Future milestones will register concrete providers.
    """

    @staticmethod
    def create_default_recommendation_engine(
        registry: RecommendationRegistry | None = None,
    ) -> RecommendationEngine:
        """Create a RecommendationEngine with default or custom registry.

        Registers SkillRecommendationProvider (priority 100) by default.

        Args:
            registry: Optional RecommendationRegistry.

        Returns:
            A fully configured RecommendationEngine ready to recommend().
        """
        reg = registry or RecommendationRegistry()
        if not reg.is_registered("SKILL"):
            from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
            reg.register(SkillRecommendationProvider())
        if not reg.is_registered("EXPERIENCE"):
            from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider
            reg.register(ExperienceRecommendationProvider())
        if not reg.is_registered("EDUCATION"):
            from ats_engine.domain.recommendation.providers.education_provider import EducationRecommendationProvider
            reg.register(EducationRecommendationProvider())
        if not reg.is_registered("PROJECT"):
            from ats_engine.domain.recommendation.providers.project_provider import ProjectRecommendationProvider
            reg.register(ProjectRecommendationProvider())
        if not reg.is_registered("CERTIFICATION"):
            from ats_engine.domain.recommendation.providers.certification_provider import CertificationRecommendationProvider
            reg.register(CertificationRecommendationProvider())
        from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine
        from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine
        from ats_engine.domain.recommendation.summary.summary_engine import ResumeIntelligenceSummaryEngine
        return RecommendationEngine(
            registry=reg,
            post_processors=[
                PrioritizationEngine(),
                RecommendationOrchestrationEngine(),
                ResumeIntelligenceSummaryEngine(),
            ],
        )
