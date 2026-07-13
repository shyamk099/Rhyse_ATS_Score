"""Project normalizer.

Purpose:
    Normalize raw project fields: split raw date pairs, and normalize URLs
    preserving their provenance, matched rule, and original values.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.project.project_models import (
    ProjectCandidate,
    NormalizedProject,
    ProjectURL,
)
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.project.exceptions import ProjectNormalizationError


class ProjectNormalizer:
    """Stateless normalizer transforming raw evidence into cleaned intermediate forms."""

    @classmethod
    def normalize(
        cls, candidate: ProjectCandidate, rules: ProjectExtractionRules
    ) -> NormalizedProject:
        """Normalize raw candidate fields and build ProjectURL objects.

        Args:
            candidate: Validated project candidate.
            rules: Configured extraction rules.

        Returns:
            The NormalizedProject metadata container.

        Raises:
            ProjectNormalizationError: If normalization encounters failures.
        """
        try:
            start_date_raw, end_date_raw = cls._split_dates(candidate, rules)

            repo_url = None
            if candidate.detected_repo_url:
                # Find matching repository rule
                matched_rule = "generic_repository_rule"
                for dom in rules.repository_domains:
                    if dom.lower() in candidate.detected_repo_url.lower():
                        matched_rule = f"repository_domain_{dom}"
                        break
                repo_url = ProjectURL(
                    original_value=candidate.detected_repo_url,
                    normalized_value=candidate.detected_repo_url.lower(),
                    matched_rule=matched_rule,
                )

            demo_url = None
            if candidate.detected_demo_url:
                # Find matching demo rule
                matched_rule = "generic_demo_rule"
                for dom in rules.demo_domains:
                    if dom.lower() in candidate.detected_demo_url.lower():
                        matched_rule = f"demo_domain_{dom}"
                        break
                demo_url = ProjectURL(
                    original_value=candidate.detected_demo_url,
                    normalized_value=candidate.detected_demo_url.lower(),
                    matched_rule=matched_rule,
                )

            return NormalizedProject(
                candidate=candidate,
                project_name=candidate.detected_name,
                organization=candidate.detected_organization,
                role=candidate.detected_role,
                start_date_raw=start_date_raw,
                end_date_raw=end_date_raw,
                duration_raw=None,
                repo_url=repo_url,
                demo_url=demo_url,
            )
        except Exception as error:
            raise ProjectNormalizationError(
                f"Failed to normalize project candidate: {error}"
            ) from error

    @classmethod
    def _split_dates(
        cls, candidate: ProjectCandidate, rules: ProjectExtractionRules
    ) -> tuple[str | None, str | None]:
        """Split detected dates into start and end date raw strings."""
        dates = list(candidate.detected_dates)
        if not dates:
            return None, None
        if len(dates) == 1:
            return dates[0], None
        return dates[0], dates[1]
