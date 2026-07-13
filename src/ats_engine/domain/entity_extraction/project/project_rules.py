"""Pydantic schemas representing configurable project extraction rules.

Purpose:
    Define configuration schemas for project titles, organization indicators,
    role indicators, demo/repository domains, and technology/confidence
    mappings loaded from the Rule Engine.
"""

from __future__ import annotations

from typing import Mapping, Sequence
from pydantic import BaseModel, ConfigDict, Field


class ProjectExtractionRules(BaseModel):
    """Configuration heuristics governing deterministic project parsing."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    extraction_scope: Sequence[str] = Field(default=("PROJECTS", "PERSONAL PROJECTS"))

    date_patterns: Sequence[str] = Field(
        default=(
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|"
            r"Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|"
            r"Dec(?:ember)?)\s+\d{4}",
            r"\d{1,2}/\d{4}",
            r"\d{4}",
        )
    )

    project_title_indicators: Sequence[str] = Field(
        default=(
            "Project", "Application", "App", "System", "Platform",
            "Tool", "Library", "Framework", "Service", "Engine",
            "Portal", "Dashboard", "Database", "Website", "Site",
            "Simulator", "Analyzer", "Bot", "Crawler", "Scraper",
        ),
    )

    organization_indicators: Sequence[str] = Field(
        default=(
            "for", "at", "client", "organization", "company", "sponsor",
            "inc", "ltd", "corp", "co", "university", "school",
        ),
    )

    role_indicators: Sequence[str] = Field(
        default=(
            "Developer", "Engineer", "Lead", "Architect", "Contributor",
            "Creator", "Author", "Designer", "Maintainer", "Manager",
        ),
    )

    repository_domains: Sequence[str] = Field(
        default=("github.com", "gitlab.com", "bitbucket.org"),
    )

    demo_domains: Sequence[str] = Field(
        default=("vercel.app", "herokuapp.com", "netlify.app", "github.io"),
    )

    technology_indicators: Sequence[str] = Field(
        default=(
            "Python", "JavaScript", "TypeScript", "React", "Node",
            "Vue", "Angular", "Java", "C\\+\\+", "Rust", "Go",
            "Docker", "AWS", "Azure", "SQL", "MongoDB", "PostgreSQL",
        ),
    )

    technology_skill_mappings: Mapping[str, str] = Field(
        default_factory=dict
    )

    confidence_mappings: Mapping[str, float] = Field(
        default={
            "PROJECTS": 0.95,
            "DEFAULT": 0.6,
        }
    )

    default_confidence: float = Field(default=0.7, ge=0.0, le=1.0)
