"""Factory for resolving and instantiating stateless format-specific parsers.

Purpose:
    Expose a unified, signature-based format detection and parser instantiation flow.
"""

from __future__ import annotations

from pathlib import Path

from ats_engine.domain.document_processing.exceptions import DocumentReadError, UnsupportedFormatError
from ats_engine.domain.document_processing.parser import DocumentParser
from ats_engine.domain.document_processing.registry import DocumentParserRegistry


class DocumentParserFactory:
    """Factory determining file formats via magic bytes signature checks and resolving parsers."""

    def __init__(self, registry: DocumentParserRegistry) -> None:
        """Initialize the factory with a parser registry."""
        self._registry = registry

    def get_parser(self, file_path: Path) -> DocumentParser:
        """Detect document format and return an instantiated parser.

        Args:
            file_path: Absolute path to the file.

        Returns:
            An instantiated, stateless DocumentParser.

        Raises:
            DocumentReadError: If the file is missing or unreadable.
            UnsupportedFormatError: If magic bytes do not match registered parsers.
        """
        if not file_path.exists():
            raise DocumentReadError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                header = f.read(4)
        except Exception as error:
            raise DocumentReadError(f"Failed to read file header signature: {error}") from error

        format_key = self._detect_format_by_signature(header)
        if not format_key:
            raise UnsupportedFormatError(
                f"Unknown magic bytes signature: {header!r}. Only PDF and DOCX are supported."
            )

        parser_cls = self._registry.get(format_key)
        if not parser_cls:
            raise UnsupportedFormatError(f"No parser registered for detected format: '{format_key}'")

        return parser_cls()

    def _detect_format_by_signature(self, header: bytes) -> str | None:
        """Analyze file header signatures to determine document formats."""
        if header.startswith(b"%PDF"):
            return "pdf"
        if header.startswith(b"PK\x03\x04"):
            return "docx"
        return None
