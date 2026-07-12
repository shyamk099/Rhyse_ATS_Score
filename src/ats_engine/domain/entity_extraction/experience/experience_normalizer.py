"""Experience normalizer.

Purpose:
    Normalize raw fields: clean company names, standardize employment types,
    and split raw date pairs into start/end components.
"""

from __future__ import annotations

import re

from ats_engine.domain.entity_extraction.experience.experience_models import (
    ExperienceCandidate,
    NormalizedExperience,
)
from ats_engine.domain.entity_extraction.experience.experience_rules import ExperienceExtractionRules
from ats_engine.domain.entity_extraction.experience.exceptions import ExperienceNormalizationError


class ExperienceNormalizer:
    """Stateless normalizer transforming raw evidence into cleaned intermediate forms."""

    @classmethod
    def normalize(
        cls, candidate: ExperienceCandidate, rules: ExperienceExtractionRules
    ) -> NormalizedExperience:
        """Normalize raw candidate fields without date interpretation.

        Args:
            candidate: Validated experience candidate.
            rules: Configured extraction rules.

        Returns:
            The NormalizedExperience metadata container.

        Raises:
            ExperienceNormalizationError: If normalization encounters failures.
        """
        try:
            # Resolve raw dates
            start_date_raw, end_date_raw = cls._split_dates(candidate, rules)

            # Detect current employment from end date text
            is_current = candidate.is_current
            if end_date_raw:
                current_indicators = [ci.lower() for ci in rules.current_employment_indicators]
                if end_date_raw.lower().strip() in current_indicators:
                    is_current = True

            return NormalizedExperience(
                candidate=candidate,
                company_name=candidate.detected_company,
                job_title=candidate.detected_title,
                employment_type=candidate.detected_employment_type,
                start_date_raw=start_date_raw,
                end_date_raw=end_date_raw,
                is_current=is_current,
            )
        except Exception as error:
            raise ExperienceNormalizationError(
                f"Failed to normalize experience candidate: {error}"
            ) from error

    @classmethod
    def _split_dates(
        cls, candidate: ExperienceCandidate, rules: ExperienceExtractionRules
    ) -> tuple[str | None, str | None]:
        """Split detected dates into start and end date raw strings.

        Uses the first detected date as start, and the second as end.
        Does NOT interpret or parse into date objects.
        """
        dates = list(candidate.detected_dates)
        if not dates:
            return None, None

        # Check the raw text for current employment indicators that may serve as end date
        text_lower = candidate.raw_text.lower()
        current_indicators = [ci.lower() for ci in rules.current_employment_indicators]

        if len(dates) == 1:
            # Check if there is a current employment indicator
            for ci in current_indicators:
                if ci in text_lower:
                    return dates[0], ci.title()
            return dates[0], None

        # Two or more dates: first is start, second is end
        return dates[0], dates[1]
