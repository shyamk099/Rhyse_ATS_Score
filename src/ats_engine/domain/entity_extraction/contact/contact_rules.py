"""Pydantic schema representing configurable contact extraction rules.

Purpose:
    Define validation rules and confidence configurations loaded from the Rule Engine.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ContactExtractionRules(BaseModel):
    """Configuration heuristics governing deterministic contact regex extractions."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    email_pattern: str = Field(
        default=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", min_length=1
    )
    phone_pattern: str = Field(
        default=r"\+?\d{1,4}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}", min_length=1
    )
    linkedin_pattern: str = Field(
        default=r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", min_length=1
    )
    github_pattern: str = Field(
        default=r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", min_length=1
    )
    portfolio_pattern: str = Field(
        default=r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[a-zA-Z0-9_.-]*)*",
        min_length=1,
    )

    email_confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    phone_confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    linkedin_confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    github_confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    portfolio_confidence: float = Field(default=0.8, ge=0.0, le=1.0)
