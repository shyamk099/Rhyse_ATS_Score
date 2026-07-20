"""AggregationValidator definition.

Purpose:
    Provide stateless pre-aggregation structural validation of a ScoreResult
    and SectionWeightConfiguration before the aggregator performs calculations.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.exceptions import AggregationValidationError


_REQUIRED_SECTIONS = (
    ("skill_score", "SKILL"),
    ("experience_score", "EXPERIENCE"),
    ("education_score", "EDUCATION"),
    ("project_score", "PROJECT"),
    ("certification_score", "CERTIFICATION"),
)


class AggregationValidator:
    """Stateless validator ensuring ScoreResult is structurally valid for aggregation.

    Validates:
        1. ScoreResult is not None.
        2. All five mandatory section scores are present and not None.
        3. Each section score has a non-None raw_score.
        4. Each section score has a valid maximum_score > 0.
        5. SectionWeightConfiguration weights sum to 1.0
           (enforced by the model itself, but validated here for defence-in-depth).
    """

    @staticmethod
    def validate(
        score_result: ScoreResult,
        weight_config: SectionWeightConfiguration,
    ) -> None:
        """Run all pre-aggregation structural checks.

        Args:
            score_result: The ScoreResult to validate.
            weight_config: The weight configuration to validate.

        Raises:
            AggregationValidationError: If any check fails.
        """
        # 1. ScoreResult must not be None
        if score_result is None:
            raise AggregationValidationError(
                "Aggregation failed: ScoreResult cannot be None."
            )

        # 2–4. Check each mandatory section
        for field, section_name in _REQUIRED_SECTIONS:
            section = getattr(score_result, field, None)

            # 2. Section must be present
            if section is None:
                raise AggregationValidationError(
                    f"Aggregation failed: mandatory section '{section_name}' "
                    f"is missing from ScoreResult."
                )

            # 3. raw_score must not be None
            if section.raw_score is None:
                raise AggregationValidationError(
                    f"Aggregation failed: section '{section_name}' has a None raw_score. "
                    f"All sections must have a numeric raw_score before aggregation."
                )

            # 4. maximum_score must be present and positive
            if section.maximum_score is None or section.maximum_score <= 0:
                raise AggregationValidationError(
                    f"Aggregation failed: section '{section_name}' has an invalid "
                    f"maximum_score ({section.maximum_score!r}). "
                    f"Must be a positive non-zero float."
                )

        # 5. Weight configuration is self-validating via Pydantic, but confirm here
        if weight_config is None:
            raise AggregationValidationError(
                "Aggregation failed: SectionWeightConfiguration cannot be None."
            )
        total = (
            weight_config.skill
            + weight_config.experience
            + weight_config.education
            + weight_config.project
            + weight_config.certification
        )
        if abs(total - 1.0) > 1e-9:
            raise AggregationValidationError(
                f"Aggregation failed: weights sum to {total:.10f}, not 1.0."
            )
