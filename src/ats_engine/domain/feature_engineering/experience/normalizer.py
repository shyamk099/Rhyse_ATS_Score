"""Structural normalization engine for Experience features.

Purpose:
    Implement structural modifications (trimming, collapsing duplicate spaces)
    without modifying job titles, company names, or other text semantics.
"""

from __future__ import annotations

import re

from ats_engine.domain.entity_extraction.experience.experience_models import ExperienceEntity
from ats_engine.domain.feature_engineering.experience.rules import ExperienceFeatureRules


class ExperienceFeatureNormalizer:
    """Stateless normalizer performing only whitespace-level cleaning of extracted fields."""

    @classmethod
    def normalize_text(cls, text: str | None) -> str | None:
        """Trim whitespace and collapse duplicate spaces inside a string.

        Args:
            text: Source string.

        Returns:
            Cleaned string.
        """
        if text is None:
            return None
        # Collapse multiple spaces into a single space, trim margins
        return re.sub(r"\s+", " ", text).strip()

    def normalize(self, entity: ExperienceEntity, rules: ExperienceFeatureRules) -> ExperienceEntity:
        """Structurally clean an Experience entity copy without altering semantic meanings.

        Args:
            entity: ExperienceEntity domain object.
            rules: Active ExperienceFeatureRules payload.

        Returns:
            A structurally cleaned copy of the ExperienceEntity.
        """
        if not rules.normalize_whitespace:
            return entity

        # Normalize simple string fields
        company_name = self.normalize_text(entity.company_name)
        job_title = self.normalize_text(entity.job_title)
        employment_type = self.normalize_text(entity.employment_type)
        start_date_raw = self.normalize_text(entity.start_date_raw)
        end_date_raw = self.normalize_text(entity.end_date_raw)
        source_text = self.normalize_text(entity.source_text) or ""

        # Normalize tuple components
        responsibilities = tuple(
            self.normalize_text(r) for r in entity.responsibilities if r is not None
        )
        technologies = tuple(
            self.normalize_text(t) for t in entity.technologies if t is not None
        )
        achievements = tuple(
            self.normalize_text(a) for a in entity.achievements if a is not None
        )

        return ExperienceEntity(
            experience_id=entity.experience_id,
            company_name=company_name,
            job_title=job_title,
            employment_type=employment_type,
            start_date_raw=start_date_raw,
            end_date_raw=end_date_raw,
            is_current=entity.is_current,
            responsibilities=responsibilities,
            technologies=technologies,
            achievements=achievements,
            confidence=entity.confidence,
            confidence_reason=entity.confidence_reason,
            matched_rules=entity.matched_rules,
            source_segment_ids=entity.source_segment_ids,
            source_text=source_text,
        )
