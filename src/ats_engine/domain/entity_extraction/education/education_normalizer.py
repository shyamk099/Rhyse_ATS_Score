"""Education normalizer.

Purpose:
    Normalize raw fields: split date pairs into start/end,
    detect graduation dates, and pass through GPA/grade as raw text.
    No date interpretation. No numeric parsing of GPA.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.education.education_models import (
    EducationCandidate,
    NormalizedEducation,
)
from ats_engine.domain.entity_extraction.education.education_rules import EducationExtractionRules
from ats_engine.domain.entity_extraction.education.exceptions import EducationNormalizationError


class EducationNormalizer:
    """Stateless normalizer transforming raw evidence into cleaned intermediate forms."""

    @classmethod
    def normalize(
        cls, candidate: EducationCandidate, rules: EducationExtractionRules
    ) -> NormalizedEducation:
        """Normalize raw candidate fields without date interpretation.

        Args:
            candidate: Validated education candidate.
            rules: Configured extraction rules.

        Returns:
            The NormalizedEducation metadata container.

        Raises:
            EducationNormalizationError: If normalization encounters failures.
        """
        try:
            start_date_raw, end_date_raw, graduation_date_raw = cls._split_dates(
                candidate, rules
            )

            return NormalizedEducation(
                candidate=candidate,
                institution_name=candidate.detected_institution,
                degree=candidate.detected_degree,
                specialization=candidate.detected_major,
                field_of_study=candidate.detected_major,
                start_date_raw=start_date_raw,
                end_date_raw=end_date_raw,
                graduation_date_raw=graduation_date_raw,
                gpa_raw=candidate.detected_gpa,
                grade_raw=candidate.detected_grade,
            )
        except Exception as error:
            raise EducationNormalizationError(
                f"Failed to normalize education candidate: {error}"
            ) from error

    @classmethod
    def _split_dates(
        cls,
        candidate: EducationCandidate,
        rules: EducationExtractionRules,
    ) -> tuple[str | None, str | None, str | None]:
        """Split detected dates into start, end, and graduation date raw strings.

        Does NOT interpret or parse into date objects.
        If a graduation indicator is present and only one date exists,
        that date is treated as the graduation date, not start date.
        """
        dates = list(candidate.detected_dates)

        if not dates:
            return None, None, None

        if len(dates) == 1:
            if candidate.has_graduation_indicator:
                return None, None, dates[0]
            return None, dates[0], None

        if len(dates) == 2:
            start = dates[0]
            end = dates[1]
            graduation = end if candidate.has_graduation_indicator else None
            return start, end, graduation

        # Three or more: first is start, second is end, third is graduation
        return dates[0], dates[1], dates[2] if len(dates) > 2 else None
