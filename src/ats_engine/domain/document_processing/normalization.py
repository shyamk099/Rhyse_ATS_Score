"""Independent text normalization pipeline.

Purpose:
    Provide reusable, modular text cleaning algorithms including Unicode NFKC mapping,
    whitespace collapsing, hyphen repair, and line-ending standardization.
"""

from __future__ import annotations

import re
import unicodedata

from ats_engine.domain.document_processing.exceptions import NormalizationError


class TextNormalizer:
    """Pipelines raw extracted strings into canonical clean representations."""

    _HORIZONTAL_SPACE_PATTERN = re.compile(r"[ \t]+")
    _HYPHEN_NEWLINE_PATTERN = re.compile(r"(\w+)-\s*\n\s*(\w+)")
    _EXCESSIVE_NEWLINE_PATTERN = re.compile(r"\n{3,}")

    @classmethod
    def normalize_line_endings(cls, text: str) -> str:
        """Standardize carriage returns and line endings to UNIX format."""
        return text.replace("\r\n", "\n").replace("\r", "\n")

    @classmethod
    def normalize_unicode(cls, text: str) -> str:
        """Apply NFKC normalization to standard compatibility forms."""
        return unicodedata.normalize("NFKC", text)

    @classmethod
    def cleanup_control_characters(cls, text: str) -> str:
        """Remove non-printable unicode control codes, preserving standard format spacing."""
        return "".join(
            char
            for char in text
            if char in ("\n", "\t") or unicodedata.category(char)[0] != "C"
        )

    @classmethod
    def cleanup_hyphens(cls, text: str) -> str:
        """Remove soft-hyphen markers and repair words broken across lines."""
        text = text.replace("\xad", "")
        return cls._HYPHEN_NEWLINE_PATTERN.sub(r"\1\2", text)

    @classmethod
    def normalize_whitespaces(cls, text: str) -> str:
        """Collapse adjacent spaces/tabs, preserving newlines."""
        lines = []
        for line in text.split("\n"):
            cleaned_line = cls._HORIZONTAL_SPACE_PATTERN.sub(" ", line).strip()
            lines.append(cleaned_line)
        return "\n".join(lines)

    @classmethod
    def normalize_empty_lines(cls, text: str) -> str:
        """Collapse multiple consecutive empty lines to a single blank separator."""
        return cls._EXCESSIVE_NEWLINE_PATTERN.sub("\n\n", text)

    @classmethod
    def normalize(cls, text: str) -> str:
        """Execute the full normalization pipeline on the raw input.

        Raises:
            NormalizationError: If text normalization fails.
        """
        try:
            cleaned = cls.normalize_line_endings(text)
            cleaned = cls.normalize_unicode(cleaned)
            cleaned = cls.cleanup_control_characters(cleaned)
            cleaned = cls.cleanup_hyphens(cleaned)
            cleaned = cls.normalize_whitespaces(cleaned)
            cleaned = cls.normalize_empty_lines(cleaned)
            return cleaned.strip()
        except Exception as error:
            raise NormalizationError(f"Normalization failed: {error}") from error
