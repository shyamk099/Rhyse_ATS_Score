"""Pydantic schemas representing configurable certification extraction rules.

Purpose:
    Define configuration schemas for certification names, issuing organization
    indicators, credential URL patterns, credential ID patterns, date patterns,
    skill mappings, and confidence thresholds loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class CertificationExtractionRules(BaseModel):
    """Configuration heuristics governing deterministic certification parsing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    extraction_scope: Sequence[str] = Field(default=("CERTIFICATIONS", "LICENSES", "AWARDS"))

    date_patterns: Sequence[str] = Field(
        default=(
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
            r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
            r"Dec(?:ember)?)\s+\d{4}",
            r"\d{1,2}/\d{4}",
            r"\d{4}",
        )
    )

    certification_indicators: Sequence[str] = Field(
        default=(
            "Certified", "Certification", "Certificate", "License", "Credential",
            "Associate", "Professional", "Expert", "Specialist", "Architect",
            "AWS", "Microsoft", "Google", "Oracle", "Cisco", "PMP", "Scrum",
        ),
    )

    issuing_organization_indicators: Sequence[str] = Field(
        default=(
            "by", "issued by", "issuer", "from", "at", "through",
            "Amazon Web Services", "Google Cloud", "Microsoft", "Oracle",
            "Cisco", "Project Management Institute", "Scrum Alliance",
        ),
    )

    credential_url_patterns: Sequence[str] = Field(
        default=(
            r"https?://(?:www\.)?credly\.com/credentials/[A-Za-z0-9_.-]+",
            r"https?://(?:www\.)?verify\.[\w.-]+",
        ),
    )

    credential_id_patterns: Sequence[str] = Field(
        default=(
            r"(?:ID|No|Number|Code)\s*[:\-]?\s*([A-Za-z0-9_\-]+)",
            r"\b[A-Z0-9]{8,12}\b",
        ),
    )

    skill_mappings: Mapping[str, str] = Field(
        default_factory=dict
    )

    confidence_mappings: Mapping[str, float] = Field(
        default={
            "CERTIFICATIONS": 0.95,
            "DEFAULT": 0.6,
        }
    )

    default_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
