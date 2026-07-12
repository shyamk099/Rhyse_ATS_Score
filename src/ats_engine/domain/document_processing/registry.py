"""Registry mapping resolved formats to stateless parser classes.

Purpose:
    Provide decoupling between format classifications and parser implementation lookups.
"""

from __future__ import annotations

from typing import Type

from ats_engine.domain.document_processing.parser import DocumentParser


class DocumentParserRegistry:
    """Registry maintaining mappings of format keys to parser class definitions."""

    def __init__(self) -> None:
        """Initialize registry with empty format mappings."""
        self._registry: dict[str, Type[DocumentParser]] = {}

    def register(self, format_key: str, parser_cls: Type[DocumentParser]) -> None:
        """Register a parser implementation for a specific format key."""
        self._registry[format_key.lower()] = parser_cls

    def get(self, format_key: str) -> Type[DocumentParser] | None:
        """Retrieve the parser class for a format key, or None if unregistered."""
        return self._registry.get(format_key.lower())
