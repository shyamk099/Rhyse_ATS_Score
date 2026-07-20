"""Explainability package boundary for Book 06 — ATS Scoring Engine.

Purpose:
    Expose ExplainabilityEngine, SectionExplanation, OverallExplanation,
    ExplainabilityResult, and ExplainabilityFormatter as the public API.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.explainability.explainer import ExplainabilityEngine
from ats_engine.domain.ats_scoring.explainability.models import (
    SectionExplanation,
    OverallExplanation,
    ExplainabilityResult,
)
from ats_engine.domain.ats_scoring.explainability.formatter import ExplainabilityFormatter

__all__ = [
    "ExplainabilityEngine",
    "SectionExplanation",
    "OverallExplanation",
    "ExplainabilityResult",
    "ExplainabilityFormatter",
]
