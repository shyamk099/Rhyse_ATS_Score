"""Section heading candidate builder.

Purpose:
    Analyze physical blocks and configured aliases to identify candidate section headers.
"""

from __future__ import annotations

from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import CanonicalDocument
from ats_engine.domain.document_processing.structure_models import BlockType as LayoutBlockType
from ats_engine.domain.entity_extraction.section.section_models import SectionCandidate
from ats_engine.domain.entity_extraction.section.section_rules import SectionDetectionRules


class SectionCandidateBuilder:
    """Stateless builder analyzing blocks and rules to discover section heading candidates."""

    @classmethod
    def find_candidates(
        cls, document: CanonicalDocument, rules: SectionDetectionRules
    ) -> Sequence[SectionCandidate]:
        """Scan layout blocks for physical headings or text matching section aliases.

        Args:
            document: The input CanonicalDocument.
            rules: The rules parameter mapping patterns.

        Returns:
            A sequence of populated SectionCandidates.
        """
        candidates: list[SectionCandidate] = []
        blocks = document.document_layout.blocks

        for idx, block in enumerate(blocks):
            text = block.raw_text.strip()
            if not text:
                continue

            normalized = text.lower()
            matched_type: str | None = None
            matched_alias: str | None = None

            # 1. Look for configured alias match
            for section_type, aliases in rules.section_aliases.items():
                for alias in aliases:
                    if normalized == alias.strip().lower():
                        matched_type = section_type
                        matched_alias = alias
                        break
                if matched_type:
                    break

            if matched_type:
                reason = (
                    f"Matched configured alias: '{matched_alias}'; "
                    f"Block matches logical type: '{matched_type}'"
                )
                candidates.append(
                    SectionCandidate(
                        block_index=idx,
                        matched_text=text,
                        section_type=matched_type,
                        confidence=rules.heading_confidence_alias_match,
                        confidence_reason=reason,
                    )
                )
                continue

            # 2. Check physical headings or heuristic heading properties
            word_count = len(text.split())
            if word_count <= rules.max_heading_words:
                is_physical_heading = block.block_type == LayoutBlockType.HEADING
                is_uppercase = text.isupper()
                no_ending_punctuation = not text.endswith((".", "?", "!"))

                if is_physical_heading or (is_uppercase and no_ending_punctuation):
                    reason = "Matched physical heading characteristics (length, punctuation, capitalization)"
                    candidates.append(
                        SectionCandidate(
                            block_index=idx,
                            matched_text=text,
                            section_type="UNKNOWN",
                            confidence=rules.heading_confidence_default,
                            confidence_reason=reason,
                        )
                    )

        return candidates
