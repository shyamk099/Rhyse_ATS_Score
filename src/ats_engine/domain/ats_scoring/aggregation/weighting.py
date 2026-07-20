"""SectionWeightConfiguration definition.

Purpose:
    Define the immutable weight configuration governing how each section
    contributes to the final overall ATS score.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ats_engine.domain.ats_scoring.exceptions import WeightConfigurationError


class SectionWeightConfiguration(BaseModel):
    """Immutable weight configuration for the five scored sections.

    Default weights (sum == 1.0):
        Skill:          35%  (0.35)
        Experience:     30%  (0.30)
        Education:      15%  (0.15)
        Project:        10%  (0.10)
        Certification:  10%  (0.10)

    All weights are stored as fractions in [0.0, 1.0].
    The sum of all five weights must equal exactly 1.0 (within floating-point epsilon).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    skill: float = Field(default=0.35, ge=0.0, le=1.0)
    experience: float = Field(default=0.30, ge=0.0, le=1.0)
    education: float = Field(default=0.15, ge=0.0, le=1.0)
    project: float = Field(default=0.10, ge=0.0, le=1.0)
    certification: float = Field(default=0.10, ge=0.0, le=1.0)
    version: str = Field(default="1.0.0", min_length=1)

    @model_validator(mode="after")
    def _validate_weights_sum(self) -> "SectionWeightConfiguration":
        """Verify that all weights sum to exactly 1.0."""
        total = self.skill + self.experience + self.education + self.project + self.certification
        if abs(total - 1.0) > 1e-9:
            raise WeightConfigurationError(
                f"Section weights must sum to 1.0, but got {total:.10f}. "
                f"(skill={self.skill}, experience={self.experience}, "
                f"education={self.education}, project={self.project}, "
                f"certification={self.certification})"
            )
        return self

    def as_dict(self) -> dict[str, float]:
        """Return a plain dict mapping section name → weight fraction."""
        return {
            "SKILL": self.skill,
            "EXPERIENCE": self.experience,
            "EDUCATION": self.education,
            "PROJECT": self.project,
            "CERTIFICATION": self.certification,
        }
