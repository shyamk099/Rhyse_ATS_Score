"""Book 07 — Recommendation Engine Package Boundary.

Purpose:
    Expose all public interfaces, engine, registry, models, providers,
    and exceptions for the Resume Intelligence Engine.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.engine import RecommendationEngine
from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.factory import RecommendationFactory
from ats_engine.domain.recommendation.models import Recommendation, RecommendationResult, RecommendationContext
from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider, RecommendationAction, BaseRecommendationValidator
from ats_engine.domain.recommendation.validator import RecommendationValidator
from ats_engine.domain.recommendation.statistics_builder import RecommendationStatisticsBuilder
from ats_engine.domain.recommendation.metadata_builder import RecommendationMetadataBuilder
from ats_engine.domain.recommendation.prioritization.models import (
    PrioritizedRecommendationResult,
    PrioritizationStatistics,
    PriorityKey,
    PriorityProfile,
)
from ats_engine.domain.recommendation.prioritization.prioritization_engine import PrioritizationEngine
from ats_engine.domain.recommendation.orchestration.models import OrchestratedRecommendationResult, OrchestrationStatistics
from ats_engine.domain.recommendation.orchestration.orchestration_engine import RecommendationOrchestrationEngine
from ats_engine.domain.recommendation.exceptions import (
    RecommendationError,
    RecommendationValidationError,
    RecommendationProviderError,
)

__all__ = [
    "RecommendationEngine",
    "RecommendationRegistry",
    "RecommendationFactory",
    "Recommendation",
    "RecommendationResult",
    "RecommendationContext",
    "BaseRecommendationProvider",
    "RecommendationAction",
    "BaseRecommendationValidator",
    "RecommendationValidator",
    "RecommendationStatisticsBuilder",
    "RecommendationMetadataBuilder",
    "PrioritizedRecommendationResult",
    "PrioritizationStatistics",
    "PriorityKey",
    "PriorityProfile",
    "PrioritizationEngine",
    "OrchestratedRecommendationResult",
    "OrchestrationStatistics",
    "RecommendationOrchestrationEngine",
    "RecommendationError",
    "RecommendationValidationError",
    "RecommendationProviderError",
]
