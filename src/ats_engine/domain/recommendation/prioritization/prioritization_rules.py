"""PrioritizationRules definition.

Purpose:
    Define deterministic priority mappings and threshold classifications.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.prioritization.models import PriorityKey, PriorityProfile


class PrioritizationRules:
    """Rules defining deterministic priority profiles for recommendation categories."""

    # Default Profile mapping keyed by PriorityKey(section, category)
    DEFAULT_MAP: dict[PriorityKey, PriorityProfile] = {
        # Skill
        PriorityKey(section="skill", category="SKILL_MISSING"): PriorityProfile(
            priority=100, impact=1.0, confidence=1.0
        ),
        PriorityKey(section="skill", category="SKILL_PARTIAL_MATCH"): PriorityProfile(
            priority=70, impact=0.75, confidence=0.95
        ),
        # Experience
        PriorityKey(section="experience", category="EXPERIENCE_MISSING"): PriorityProfile(
            priority=95, impact=0.90, confidence=1.0
        ),
        PriorityKey(section="experience", category="EXPERIENCE_PARTIAL_MATCH"): PriorityProfile(
            priority=65, impact=0.50, confidence=0.90
        ),
        PriorityKey(section="experience", category="EXPERIENCE_DURATION_GAP"): PriorityProfile(
            priority=65, impact=0.50, confidence=0.95
        ),
        # Education
        PriorityKey(section="education", category="EDUCATION_MISSING"): PriorityProfile(
            priority=90, impact=0.90, confidence=1.0
        ),
        PriorityKey(section="education", category="EDUCATION_PARTIAL_MATCH"): PriorityProfile(
            priority=55, impact=0.50, confidence=0.90
        ),
        PriorityKey(section="education", category="EDUCATION_LEVEL_GAP"): PriorityProfile(
            priority=90, impact=0.75, confidence=0.95
        ),
        # Project
        PriorityKey(section="project", category="PROJECT_MISSING"): PriorityProfile(
            priority=80, impact=0.75, confidence=1.0
        ),
        PriorityKey(section="project", category="PROJECT_PARTIAL_MATCH"): PriorityProfile(
            priority=60, impact=0.50, confidence=0.90
        ),
        PriorityKey(section="project", category="PROJECT_RELATED_GAP"): PriorityProfile(
            priority=60, impact=0.50, confidence=0.95
        ),
        # Certification
        PriorityKey(section="certification", category="CERTIFICATION_MISSING"): PriorityProfile(
            priority=85, impact=0.75, confidence=1.0
        ),
        PriorityKey(section="certification", category="CERTIFICATION_PARTIAL_MATCH"): PriorityProfile(
            priority=55, impact=0.50, confidence=0.90
        ),
        PriorityKey(section="certification", category="CERTIFICATION_EXPIRED"): PriorityProfile(
            priority=85, impact=0.90, confidence=0.95
        ),
    }

    # Threshold limits
    HIGH_THRESHOLD: int = 85
    MEDIUM_THRESHOLD: int = 70

    def __init__(self, profile_map: dict[PriorityKey, PriorityProfile] | None = None) -> None:
        """Initialize rules with custom or default profile mapping."""
        self._map = profile_map or self.DEFAULT_MAP

    def resolve_profile(self, section: str, category: str) -> PriorityProfile:
        """Retrieve priority profile for the given section and category.

        Falls back to a default profile if not found in mapping.
        """
        key = PriorityKey(section=section, category=category)
        if key in self._map:
            return self._map[key]
        # Safe default fallback
        return PriorityProfile(priority=50, impact=0.50, confidence=0.90)

    def is_high(self, priority: int) -> bool:
        """Check if priority is high classification."""
        return priority >= self.HIGH_THRESHOLD

    def is_medium(self, priority: int) -> bool:
        """Check if priority is medium classification."""
        return self.MEDIUM_THRESHOLD <= priority < self.HIGH_THRESHOLD

    def is_low(self, priority: int) -> bool:
        """Check if priority is low classification."""
        return priority < self.MEDIUM_THRESHOLD
