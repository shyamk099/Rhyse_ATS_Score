"""Project candidate validator.

Purpose:
    Validate that a project candidate has minimum required evidence
    (at least a project name or role detected).
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.project.project_models import ProjectCandidate
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules


class ProjectCandidateValidator:
    """Stateless validator checking project candidates for minimum evidence."""

    @classmethod
    def validate(cls, candidate: ProjectCandidate, rules: ProjectExtractionRules) -> bool:
        """Validate that candidate contains minimal meaningful evidence.

        Args:
            candidate: Discovered project candidate.
            rules: Configured extraction rules.

        Returns:
            True if candidate has sufficient evidence, False otherwise.
        """
        has_name = candidate.detected_name is not None
        has_role = candidate.detected_role is not None

        # Require at least a name or role to form a valid project entry
        if has_name or has_role:
            return True

        return False
