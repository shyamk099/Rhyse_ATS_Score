"""Orchestrator package for Book 06 — ATS Scoring Engine.

Purpose:
    Expose ScoreOrchestrator, ExecutionPlan, ScoreOrchestratorValidator,
    and OrchestratorStatisticsBuilder as the public orchestration API.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.orchestrator.orchestrator import ScoreOrchestrator
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan, ExecutionPlanEntry
from ats_engine.domain.ats_scoring.orchestrator.validator import ScoreOrchestratorValidator
from ats_engine.domain.ats_scoring.orchestrator.statistics_builder import OrchestratorStatisticsBuilder

__all__ = [
    "ScoreOrchestrator",
    "ExecutionPlan",
    "ExecutionPlanEntry",
    "ScoreOrchestratorValidator",
    "OrchestratorStatisticsBuilder",
]
