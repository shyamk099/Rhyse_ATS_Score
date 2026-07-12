"""Document cross-model consistency validator.

Purpose:
    Audit relationship integrity and character content equivalence between NormalizedDocument,
    DocumentLayout, and SegmentCollection.
"""

from __future__ import annotations

from ats_engine.domain.document_processing.exceptions import ConsistencyValidationError
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import DocumentLayout
from ats_engine.domain.document_processing.segmentation_models import SegmentCollection
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules


class DocumentConsistencyValidator:
    """Stateless validator confirming content parity across layout and segments."""

    @classmethod
    def validate(
        cls,
        normalized: NormalizedDocument,
        layout: DocumentLayout,
        segments: SegmentCollection,
        rules: CanonicalValidationRules,
    ) -> None:
        """Audit the parsed models for content consistency and block mappings.

        Args:
            normalized: The NormalizedDocument.
            layout: The DocumentLayout.
            segments: The SegmentCollection.
            rules: The rules parameter mapping thresholds.

        Raises:
            ConsistencyValidationError: If counts, content parity, or block links are inconsistent.
        """
        # 1. Minimum character validations
        normalized_chars = len(normalized.cleaned_content)
        if normalized_chars < rules.min_allowed_characters:
            raise ConsistencyValidationError(
                f"Document text length {normalized_chars} is below minimum requirement {rules.min_allowed_characters}."
            )

        # 2. Content equivalence validation (non-whitespace text matching)
        normalized_stripped = "".join(normalized.cleaned_content.split())
        segments_stripped = "".join("".join(seg.text_content.split()) for seg in segments.segments)

        if rules.enable_variance_tolerance:
            variance = abs(len(normalized_stripped) - len(segments_stripped)) / max(len(normalized_stripped), 1)
            if variance > rules.allowable_character_count_variance:
                raise ConsistencyValidationError(
                    f"Character variance {variance:.4f} exceeds permitted tolerance {rules.allowable_character_count_variance}."
                )
        else:
            if normalized_stripped != segments_stripped:
                raise ConsistencyValidationError(
                    f"Character content mismatch: Normalized length={len(normalized_stripped)}, "
                    f"Segments length={len(segments_stripped)} (excluding whitespaces)."
                )

        # 3. Block reference completeness audits
        layout_block_keys = {cls._block_key(b) for b in layout.blocks}
        segment_block_keys: list[str] = []

        for segment in segments.segments:
            for block in segment.associated_blocks:
                key = cls._block_key(block)
                if key in segment_block_keys:
                    raise ConsistencyValidationError(f"Duplicate block reference in segment collection: {key}.")
                segment_block_keys.append(key)

        segment_block_keys_set = set(segment_block_keys)

        missing_blocks = layout_block_keys - segment_block_keys_set
        if missing_blocks:
            raise ConsistencyValidationError(f"Layout blocks missing from physical segments: {missing_blocks}.")

        extra_blocks = segment_block_keys_set - layout_block_keys
        if extra_blocks:
            raise ConsistencyValidationError(f"Segment references block not present in Layout: {extra_blocks}.")

    @classmethod
    def _block_key(cls, block) -> str:
        if not block.lines:
            return "empty_block"
        first_line = block.lines[0]
        return f"{first_line.page_number}_{first_line.line_number}"
