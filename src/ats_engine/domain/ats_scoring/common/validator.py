"""ScoreValidator definition.

Purpose:
    Provide stateless read-only validation of CanonicalMatchCollections and rules.
"""

from __future__ import annotations

from ats_engine.domain.matching.models import CanonicalMatchCollection
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.exceptions import ScoringValidationError
from ats_engine.domain.ats_scoring.constants import SUPPORTED_SCORERS


class ScoreValidator:
    """Stateless validator implementing structural and version constraint checks on match collections."""

    @staticmethod
    def validate(
        match_collection: CanonicalMatchCollection,
        rules: ScoringRules,
    ) -> None:
        """Inspect and validate CanonicalMatchCollection and ScoringRules.

        Raises:
            ScoringValidationError: If validation constraints are violated.
        """
        if match_collection is None:
            raise ScoringValidationError("CanonicalMatchCollection cannot be None.")

        # Validate statistics and summary blocks presence
        if not hasattr(match_collection, "validation_summary") or match_collection.validation_summary is None:
            raise ScoringValidationError("CanonicalMatchCollection validation summary is missing.")

        if not hasattr(match_collection, "statistics") or match_collection.statistics is None:
            raise ScoringValidationError("CanonicalMatchCollection statistics block is missing.")

        # Supported categories check
        if match_collection.results:
            for result in match_collection.results:
                matcher_type = getattr(result, "matcher_type", None)
                if not matcher_type:
                    raise ScoringValidationError("MatchResult is missing required 'matcher_type'.")

                norm_type = matcher_type.replace("Matcher", "").upper()
                if norm_type not in SUPPORTED_SCORERS:
                    raise ScoringValidationError(
                        f"Unsupported matcher category in results: {matcher_type}"
                    )

        # Version compatibility check
        if not rules or not rules.version:
            raise ScoringValidationError("ScoringRules configuration is missing or invalid.")

        if rules.version != "1.0.0":
            raise ScoringValidationError(
                f"Scoring rules version '{rules.version}' is incompatible with engine version '1.0.0'."
            )
