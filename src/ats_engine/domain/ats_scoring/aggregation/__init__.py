"""Aggregation package for Book 06 — ATS Scoring Engine.

Purpose:
    Expose OverallScoreAggregator, SectionWeightConfiguration, ScoreNormalizer,
    AggregationValidator, and AggregationStatisticsBuilder as the public aggregation API.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.aggregation.aggregator import OverallScoreAggregator
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.aggregation.normalization import ScoreNormalizer
from ats_engine.domain.ats_scoring.aggregation.validator import AggregationValidator
from ats_engine.domain.ats_scoring.aggregation.statistics_builder import AggregationStatisticsBuilder

__all__ = [
    "OverallScoreAggregator",
    "SectionWeightConfiguration",
    "ScoreNormalizer",
    "AggregationValidator",
    "AggregationStatisticsBuilder",
]
