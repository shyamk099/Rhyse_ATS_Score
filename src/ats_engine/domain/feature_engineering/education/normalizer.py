"""Structural normalization engine for Education features.

Purpose:
    Implement structural modifications (trimming, collapsing duplicate spaces)
    without modifying institution names, degree titles, or other text semantics.
"""

from __future__ import annotations

import re

from ats_engine.domain.entity_extraction.education.education_models import EducationEntity
from ats_engine.domain.feature_engineering.education.rules import EducationFeatureRules


class EducationFeatureNormalizer:
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

    def normalize(self, entity: EducationEntity, rules: EducationFeatureRules) -> EducationEntity:
        """Structurally clean an Education entity copy without altering semantic meanings.

        Args:
            entity: EducationEntity domain object.
            rules: Active EducationFeatureRules payload.

        Returns:
            A structurally cleaned copy of the EducationEntity.
        """
        if not rules.normalize_whitespace:
            return entity

        # Normalize simple string fields
        institution_name = self.normalize_text(entity.institution_name)
        degree = self.normalize_text(entity.degree)
        specialization = self.normalize_text(entity.specialization)
        field_of_study = self.normalize_text(entity.field_of_study)
        start_date_raw = self.normalize_text(entity.start_date_raw)
        end_date_raw = self.normalize_text(entity.end_date_raw)
        graduation_date_raw = self.normalize_text(entity.graduation_date_raw)
        gpa_raw = self.normalize_text(entity.gpa_raw)
        grade_raw = self.normalize_text(entity.grade_raw)
        location_raw = self.normalize_text(entity.location_raw)
        source_text = self.normalize_text(entity.source_text) or ""

        # Normalize tuple components
        honors = tuple(
            self.normalize_text(h) for h in entity.honors if h is not None
        )
        certifications = tuple(
            self.normalize_text(c) for c in entity.certifications if c is not None
        )

        return EducationEntity(
            education_id=entity.education_id,
            institution_name=institution_name,
            degree=degree,
            specialization=specialization,
            field_of_study=field_of_study,
            start_date_raw=start_date_raw,
            end_date_raw=end_date_raw,
            graduation_date_raw=graduation_date_raw,
            gpa_raw=gpa_raw,
            grade_raw=grade_raw,
            honors=honors,
            certifications=certifications,
            location_raw=location_raw,
            confidence=entity.confidence,
            confidence_reason=entity.confidence_reason,
            matched_rules=entity.matched_rules,
            source_segment_ids=entity.source_segment_ids,
            source_text=source_text,
        )
