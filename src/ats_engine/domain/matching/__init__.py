"""Domain matching module initialization.

Purpose:
    Expose base matching engine constructs, service interfaces,
    and schemas for downstream consumption.
"""

from __future__ import annotations

from ats_engine.domain.matching.exceptions import (
    ContextValidationError,
    MatcherRegistrationError,
    MatchingError,
    PipelineExecutionError,
    UnknownMatcherError,
)
from ats_engine.domain.matching.factory import FeatureMatcherFactory
from ats_engine.domain.matching.matcher import FeatureMatcher
from ats_engine.domain.matching.models import (
    MatchCollection,
    MatchingContext,
    MatchingStatistics,
    MatchLocation,
    MatchMetadata,
    MatchResult,
)
from ats_engine.domain.matching.pipeline import MatchingPipeline
from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.rules import MatchingRules
from ats_engine.domain.matching.service import MatchingService

__all__ = [
    "FeatureMatcher",
    "MatchingService",
    "MatchingPipeline",
    "FeatureMatcherRegistry",
    "FeatureMatcherFactory",
    "MatchingRules",
    "MatchLocation",
    "MatchMetadata",
    "MatchResult",
    "MatchingStatistics",
    "MatchingContext",
    "MatchCollection",
    "MatchingError",
    "UnknownMatcherError",
    "MatcherRegistrationError",
    "PipelineExecutionError",
    "ContextValidationError",
]
