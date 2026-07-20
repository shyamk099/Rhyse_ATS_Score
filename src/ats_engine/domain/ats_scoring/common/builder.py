"""ScoringContextBuilder definition.

Purpose:
    Provide context construction for scoring pipeline executions.
"""

from __future__ import annotations

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext


class ScoringContextBuilder:
    """Builder compiling match collection and configuration rules into a ScoringContext DTO."""

    @staticmethod
    def build(
        match_collection: CanonicalMatchCollection,
        rules: ScoringRules,
    ) -> ScoringContext:
        """Construct an immutable, frozen ScoringContext DTO."""
        return ScoringContext(
            match_collection=match_collection,
            rules=rules,
        )

