"""ScoringFactory definition.

Purpose:
    Expose construction builders for registries, pipelines, and rules configuration.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.rules import ScoringRules


class ScoringFactory:
    """Factory handling dependency injection initialization for Scoring registry and pipeline."""

    @staticmethod
    def create_default_registry() -> ScoringRegistry:
        """Create and return a new empty ScoringRegistry instance pre-populated with defaults."""
        from ats_engine.domain.ats_scoring.skill.scorer import SkillScorer
        from ats_engine.domain.ats_scoring.experience.scorer import ExperienceScorer
        from ats_engine.domain.ats_scoring.education.scorer import EducationScorer
        from ats_engine.domain.ats_scoring.project.scorer import ProjectScorer
        from ats_engine.domain.ats_scoring.certification.scorer import CertificationScorer
        reg = ScoringRegistry()
        reg.register("SKILL", SkillScorer, priority=100, enabled=True)
        reg.register("EXPERIENCE", ExperienceScorer, priority=200, enabled=True)
        reg.register("EDUCATION", EducationScorer, priority=300, enabled=True)
        reg.register("PROJECT", ProjectScorer, priority=400, enabled=True)
        reg.register("CERTIFICATION", CertificationScorer, priority=500, enabled=True)
        return reg

    @staticmethod
    def create_default_pipeline(registry: ScoringRegistry | None = None) -> ScoringPipeline:
        """Create a new ScoringPipeline instance, injecting a registry."""
        reg = registry or ScoringFactory.create_default_registry()
        return ScoringPipeline(registry=reg)

    @staticmethod
    def create_default_rules() -> ScoringRules:
        """Create and return a default ScoringRules configuration."""
        return ScoringRules()

    @staticmethod
    def create_default_orchestrator(
        registry: "ScoringRegistry | None" = None,
    ) -> "ScoreOrchestrator":
        """Create a ScoreOrchestrator wired with the default registry and pipeline.

        Args:
            registry: Optional pre-built registry. Falls back to create_default_registry().

        Returns:
            A fully configured ScoreOrchestrator ready to orchestrate() a CanonicalMatchCollection.
        """
        from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
        reg = registry or ScoringFactory.create_default_registry()
        pipeline = ScoringFactory.create_default_pipeline(reg)
        return ScoreOrchestrator(pipeline=pipeline, registry=reg)

    @staticmethod
    def create_default_aggregator(
        weight_config: "SectionWeightConfiguration | None" = None,
    ) -> "OverallScoreAggregator":
        """Create an OverallScoreAggregator with default or custom weight configuration.

        Args:
            weight_config: Optional SectionWeightConfiguration. Defaults to standard
                weights (Skill 35%, Experience 30%, Education 15%, Project 10%,
                Certification 10%) if not provided.

        Returns:
            A fully configured OverallScoreAggregator ready to aggregate() a ScoreResult.
        """
        from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
        from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
        wc = weight_config or SectionWeightConfiguration()
        return OverallScoreAggregator(weight_config=wc)

    @staticmethod
    def create_default_explainer(
        weight_config: "SectionWeightConfiguration | None" = None,
    ) -> "ExplainabilityEngine":
        """Create an ExplainabilityEngine wired with the default or custom weights.

        Args:
            weight_config: Optional SectionWeightConfiguration.

        Returns:
            A configured ExplainabilityEngine ready to explain() a ScoreResult.
        """
        from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
        from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
        wc = weight_config or SectionWeightConfiguration()
        return ExplainabilityEngine(weight_config=wc)

