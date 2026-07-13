"""Certification assembler.

Purpose:
    Group normalized certification evidence into compound AssembledCertification records.
    Assigns canonical certification IDs (CERT-XXXXXXXX). Resolves skill mappings.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.entity_extraction.certification.certification_models import (
    AssembledCertification,
    NormalizedCertification,
)
from ats_engine.domain.entity_extraction.certification.certification_rules import CertificationExtractionRules


class CertificationAssembler:
    """Stateless assembler grouping evidence and assigning canonical certification IDs."""

    @classmethod
    def assemble(
        cls,
        normalized_list: Sequence[NormalizedCertification],
        rules: CertificationExtractionRules,
    ) -> Sequence[AssembledCertification]:
        """Group normalized certification candidates into compound records.

        Args:
            normalized_list: Pre-validated normalized certification instances.
            rules: Configured extraction rules.

        Returns:
            A sequence of AssembledCertification records.
        """
        assembled: list[AssembledCertification] = []

        for idx, norm in enumerate(normalized_list, start=1):
            certification_id = f"CERT-{idx:08d}"

            # Extract skills and map to Skill IDs if present
            skill_ids, raw_skills = cls._extract_skills(norm.candidate.raw_text, rules)

            # Heuristically extract description (extra lines after the first line)
            description = cls._extract_description(norm.candidate.raw_text)

            assembled.append(
                AssembledCertification(
                    certification_id=certification_id,
                    certification_name=norm.certification_name,
                    issuing_organization=norm.issuing_organization,
                    credential_id_raw=norm.credential_id_raw,
                    credential_url=norm.credential_url,
                    issue_date_raw=norm.issue_date_raw,
                    expiration_date_raw=norm.expiration_date_raw,
                    validity_status_raw=None,
                    associated_skill_ids=tuple(skill_ids),
                    associated_skills_raw=tuple(raw_skills),
                    description_raw=description,
                    source_segment_ids=(norm.candidate.segment_id,),
                    source_text=norm.candidate.raw_text,
                )
            )

        return assembled

    @classmethod
    def _extract_skills(
        cls, raw_text: str, rules: CertificationExtractionRules
    ) -> tuple[list[str], list[str]]:
        """Extract skills mentioned in text and partition into Skill IDs vs raw skills."""
        skill_ids: list[str] = []
        raw_skills: list[str] = []
        text_lower = raw_text.lower()

        # Check mapping keys in the rule configuration
        for skill_term, canonical_id in rules.skill_mappings.items():
            pattern = re.compile(rf"\b{re.escape(skill_term)}\b", re.IGNORECASE)
            if pattern.search(text_lower):
                skill_ids.append(canonical_id)

        # If a term is matched but no canonical ID is resolved, it goes to raw_skills.
        # For testing, we can check for skill indicators or keywords like "in python" or "for scrum"
        # and if they aren't in skill_mappings, append them to raw_skills.
        # Let's extract any word following "in" or "for" as a raw skill if not resolved.
        pattern_in = re.compile(r"\b(?:in|using|with)\b\s+([A-Za-z0-9+#]+)", re.IGNORECASE)
        for match in pattern_in.finditer(raw_text):
            val = match.group(1).strip()
            # Verify it's not already resolved
            val_lower = val.lower()
            if val_lower not in rules.skill_mappings:
                if len(val) > 2 and val_lower not in [s.lower() for s in raw_skills]:
                    raw_skills.append(val)

        return skill_ids, raw_skills

    @classmethod
    def _extract_description(cls, raw_text: str) -> str | None:
        """Extract description from certification text (subsequent lines)."""
        lines = raw_text.split("\n")
        if len(lines) > 1:
            desc = " ".join([l.strip() for l in lines[1:] if l.strip()]).strip()
            return desc if desc else None
        return None
