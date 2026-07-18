"""Abstract matcher interface.

Purpose:
    Define base FeatureMatcher class that all domain-specific matching components
    inherit and implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from ats_engine.domain.feature_engineering.models import Feature
from ats_engine.domain.matching.models import MatchingContext, MatchResult


class FeatureMatcher(ABC):
    """Abstract interface defining required contract for comparing feature segments."""

    @abstractmethod
    def match(
        self,
        resume_features: Sequence[Feature],
        job_features: Sequence[Feature],
        context: MatchingContext,
    ) -> Sequence[MatchResult]:
        """Perform comparison matches across resume and job feature sequences.

        Args:
            resume_features: Extracted features from resume.
            job_features: Extracted features from job description.
            context: Context attributes governing rules and metadata.

        Returns:
            A sequence of populated MatchResult DTOs.
        """
        pass
