"""ScoreNormalizer definition.

Purpose:
    Provide stateless per-section score normalization.

Formula:
    normalized = (raw_score / maximum_score) × 100

Result is clamped to [0.0, 100.0].
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.models.section_score import SectionScore
from ats_engine.domain.ats_scoring.models.score_result import ScoreResult
from ats_engine.domain.ats_scoring.exceptions import NormalizationError


_SECTION_FIELDS = (
    "skill_score",
    "experience_score",
    "education_score",
    "project_score",
    "certification_score",
)


class ScoreNormalizer:
    """Stateless normalizer applying the formula: (raw / maximum) × 100.

    Rules:
        - maximum_score must be present and > 0, otherwise NormalizationError is raised.
        - raw_score None is treated as 0.0.
        - Result is clamped to [0.0, 100.0].
        - Normalization is idempotent — calling twice gives the same result.
    """

    @staticmethod
    def normalize(section_score: SectionScore) -> float:
        """Normalize a single SectionScore to a value in [0.0, 100.0].

        Args:
            section_score: The SectionScore to normalize.

        Returns:
            A float in [0.0, 100.0] representing the normalized score.

        Raises:
            NormalizationError: If maximum_score is None or zero.
        """
        maximum = section_score.maximum_score
        if maximum is None or maximum == 0.0:
            raise NormalizationError(
                f"Cannot normalize section '{section_score.section_name}': "
                f"maximum_score is {maximum!r}. Must be a positive non-zero float."
            )

        raw = section_score.raw_score if section_score.raw_score is not None else 0.0
        normalized = (raw / maximum) * 100.0
        # Clamp to [0.0, 100.0]
        return max(0.0, min(100.0, normalized))

    @staticmethod
    def normalize_all(score_result: ScoreResult) -> dict[str, float]:
        """Normalize all five section scores and return a mapping.

        Args:
            score_result: The ScoreResult containing all section scores.

        Returns:
            A dict mapping section name (e.g. "SKILL") → normalized float [0.0, 100.0].

        Raises:
            NormalizationError: If any section score cannot be normalized.
        """
        name_map = {
            "skill_score": "SKILL",
            "experience_score": "EXPERIENCE",
            "education_score": "EDUCATION",
            "project_score": "PROJECT",
            "certification_score": "CERTIFICATION",
        }
        result: dict[str, float] = {}
        for field, section_name in name_map.items():
            section = getattr(score_result, field, None)
            if section is None:
                raise NormalizationError(
                    f"Cannot normalize: section '{section_name}' is missing from ScoreResult."
                )
            result[section_name] = ScoreNormalizer.normalize(section)
        return result
