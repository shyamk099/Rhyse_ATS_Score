"""Canonical document builder.

Purpose:
    Expose helper routines to compile CanonicalMetadata containers from raw document objects.
"""

from __future__ import annotations

import uuid

from ats_engine.domain.document_processing.canonical_models import CanonicalMetadata
from ats_engine.domain.document_processing.models import RawDocument


class CanonicalDocumentBuilder:
    """Stateless builder compiling metadata schemas for the canonical envelope."""

    @classmethod
    def build_metadata(
        cls, raw_document: RawDocument, page_count: int, parser_used: str
    ) -> CanonicalMetadata:
        """Create a new CanonicalMetadata instance with a generated canonical ID.

        Args:
            raw_document: The source RawDocument.
            page_count: Validated page count.
            parser_used: Class name of the parser employed.

        Returns:
            A populated, immutable CanonicalMetadata instance.
        """
        canonical_id = f"doc_{uuid.uuid4().hex[:12]}"
        return CanonicalMetadata(
            canonical_id=canonical_id,
            source_filename=raw_document.filename,
            file_size_bytes=raw_document.file_size_bytes,
            page_count=page_count,
            parser_used=parser_used,
            encoding="utf-8",
        )
