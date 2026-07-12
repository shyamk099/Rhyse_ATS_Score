"""Parser interface protocol.

Purpose:
    Define the stateless contract for format-specific document extraction components.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from ats_engine.domain.document_processing.models import RawDocument


@runtime_checkable
class DocumentParser(Protocol):
    """Protocol establishing stateless parsing behavior for format extractors."""

    def parse(self, file_path: Path) -> RawDocument:
        """Extract raw content from a file and compile a RawDocument.

        Args:
            file_path: Path to the target document.

        Returns:
            An immutable RawDocument containing raw text and structure pages.

        Raises:
            CorruptedDocumentError: If the document is corrupted or unreadable.
            DocumentReadError: If access to the file fails.
        """
        ...
