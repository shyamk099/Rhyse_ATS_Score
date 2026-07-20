"""Book 06 — ATS Scoring Engine Package Boundary.

Purpose:
    Expose all public interfaces, service facades, pipeline orchestrators, and DTO models.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.interfaces import AbstractScorer, BaseSectionScorer, AbstractClassificationResolver
from ats_engine.domain.ats_scoring.exceptions import (
    ScoringError,
    ScoringValidationError,
    ScoringPipelineError,
    ScorerRegistrationError,
    UnsupportedScorerError,
    ScoreBuildError,
    SkillScoringError,
    SkillValidationError,
    ExperienceScoringError,
    ExperienceValidationError,
    EducationScoringError,
    EducationValidationError,
    ProjectScoringError,
    ProjectValidationError,
    CertificationScoringError,
    CertificationValidationError,
    OrchestrationError,
    ExecutionPlanError,
    RegistryValidationError,
    AggregationError,
    NormalizationError,
    WeightConfigurationError,
    AggregationValidationError,
    ExplainabilityError,
    FormattingError,
    ExplainabilityValidationError,
)
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.factory import ScoringFactory
from ats_engine.domain.ats_scoring.pipeline import ScoringPipeline
from ats_engine.domain.ats_scoring.service import ScoringService
from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan, ExecutionPlanEntry
from ats_engine.domain.ats_scoring.orchestrator.validator import ScoreOrchestratorValidator
from ats_engine.domain.ats_scoring.orchestrator.statistics_builder import OrchestratorStatisticsBuilder
from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.aggregation.normalization import ScoreNormalizer
from ats_engine.domain.ats_scoring.aggregation.validator import AggregationValidator
from ats_engine.domain.ats_scoring.aggregation.statistics_builder import AggregationStatisticsBuilder
from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from ats_engine.domain.ats_scoring.explainability.models import (
    SectionExplanation,
    OverallExplanation,
    ExplainabilityResult,
)
from ats_engine.domain.ats_scoring.explainability.formatter import ExplainabilityFormatter

from ats_engine.domain.ats_scoring.models.score_breakdown import ScoreBreakdown
from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_statistics import ScoreStatistics
from ats_engine.domain.ats_scoring.models.score_metadata import ScoreMetadata
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext

__all__ = [
    "AbstractScorer",
    "BaseSectionScorer",
    "AbstractClassificationResolver",
    "ScoringRules",
    "ScoringRegistry",
    "ScoringFactory",
    "ScoringPipeline",
    "ScoringService",
    "ScoreOrchestrator",
    "ExecutionPlan",
    "ExecutionPlanEntry",
    "ScoreOrchestratorValidator",
    "OrchestratorStatisticsBuilder",
    "ScoreBreakdown",
    "SectionScore",
    "ScoreStatistics",
    "ScoreMetadata",
    "ScoreResult",
    "ScoringContext",
    "ScoringError",
    "ScoringValidationError",
    "ScoringPipelineError",
    "ScorerRegistrationError",
    "UnsupportedScorerError",
    "ScoreBuildError",
    "SkillScoringError",
    "SkillValidationError",
    "ExperienceScoringError",
    "ExperienceValidationError",
    "EducationScoringError",
    "EducationValidationError",
    "ProjectScoringError",
    "ProjectValidationError",
    "CertificationScoringError",
    "CertificationValidationError",
    "OrchestrationError",
    "ExecutionPlanError",
    "RegistryValidationError",
    "OverallScoreAggregator",
    "SectionWeightConfiguration",
    "ScoreNormalizer",
    "AggregationValidator",
    "AggregationStatisticsBuilder",
    "AggregationError",
    "NormalizationError",
    "WeightConfigurationError",
    "AggregationValidationError",
    "ExplainabilityEngine",
    "SectionExplanation",
    "OverallExplanation",
    "ExplainabilityResult",
    "ExplainabilityFormatter",
    "ExplainabilityError",
    "FormattingError",
    "ExplainabilityValidationError",
]
