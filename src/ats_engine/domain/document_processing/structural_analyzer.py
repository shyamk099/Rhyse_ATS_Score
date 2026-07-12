"""Stateless structural layout analyzer.

Purpose:
    Perform physical line extraction, block grouping, and reading-order analysis on parsed texts.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.document_processing.exceptions import NormalizationError
from ats_engine.domain.document_processing.models import NormalizedDocument, RawDocument
from ats_engine.domain.document_processing.structure_models import (
    BlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.structural_rules import StructuralAnalysisRules


class StructuralAnalyzer:
    """Stateless analyzer decomposing normalized content into physical layout hierarchies."""

    def __init__(self, rules: StructuralAnalysisRules) -> None:
        """Initialize the analyzer with configurable heuristics."""
        self._rules = rules
        self._numbered_regexes = [re.compile(pat) for pat in rules.numbered_patterns]

    def analyze(self, raw_document: RawDocument, normalized_document: NormalizedDocument) -> DocumentLayout:
        """Decompose a normalized document's content into physical blocks.

        Args:
            raw_document: The raw document containing file size and page segments.
            normalized_document: The clean text content document.

        Returns:
            An immutable DocumentLayout container mapping the physical reading order.
        """
        # Process lines page-by-page if page arrays exist, otherwise fall back to full content as page 1
        pages = raw_document.pages if raw_document.pages else (normalized_document.cleaned_content,)
        
        physical_lines: list[PhysicalLine] = []
        global_line_number = 1

        for page_idx, page_content in enumerate(pages, start=1):
            for raw_line in page_content.split("\n"):
                stripped = raw_line.strip()
                if not stripped:
                    continue
                
                # Detect leading whitespace for indentation
                indentation = len(raw_line) - len(raw_line.lstrip())
                
                line = PhysicalLine(
                    text=stripped,
                    line_number=global_line_number,
                    page_number=page_idx,
                    indentation_spaces=indentation,
                    character_count=len(stripped),
                )
                physical_lines.append(line)
                global_line_number += 1

        blocks = self._group_lines_into_blocks(physical_lines)
        
        return DocumentLayout(
            blocks=tuple(blocks),
            total_blocks=len(blocks),
            total_lines=len(physical_lines),
        )

    def _group_lines_into_blocks(self, lines: list[PhysicalLine]) -> list[PhysicalBlock]:
        """Aggregate sequential lines sharing physical characteristics into cohesive layout blocks."""
        if not lines:
            return []

        blocks: list[PhysicalBlock] = []
        current_block_type: BlockType | None = None
        current_lines: list[PhysicalLine] = []

        for line in lines:
            line_type = self._classify_line(line)
            
            # Flush existing block if block boundary/type changes
            if current_block_type is not None and (
                line_type != current_block_type or line_type == BlockType.HEADING
            ):
                blocks.append(self._compile_block(current_block_type, current_lines))
                current_lines = []

            current_block_type = line_type
            current_lines.append(line)

        # Flush the final block
        if current_lines and current_block_type is not None:
            blocks.append(self._compile_block(current_block_type, current_lines))

        return blocks

    def _classify_line(self, line: PhysicalLine) -> BlockType:
        """Apply configured physical heuristics to determine layout categories."""
        text = line.text

        # 1. Check for bullet list indicators
        if any(text.startswith(bullet) for bullet in self._rules.bullet_symbols):
            return BlockType.LIST

        # 2. Check for numbered lists
        if any(regex.match(text) for regex in self._numbered_regexes):
            return BlockType.LIST

        # 3. Check for physical table lines (e.g. delimiters repeating above threshold)
        for delimiter in self._rules.table_delimiters:
            if text.count(delimiter) >= self._rules.table_min_delimiters:
                return BlockType.TABLE

        # 4. Check for physical headings (capitalization, length limits, absence of sentence end punctuation)
        if len(text) <= self._rules.max_heading_length:
            is_all_caps = text.isupper() if self._rules.heading_all_caps else False
            no_punctuation = not text.endswith((".", "?", "!"))
            
            if is_all_caps or no_punctuation:
                return BlockType.HEADING

        return BlockType.TEXT

    def _compile_block(self, block_type: BlockType, lines: list[PhysicalLine]) -> PhysicalBlock:
        """Create an immutable PhysicalBlock from a line sequence."""
        raw_text = "\n".join(line.text for line in lines)
        return PhysicalBlock(
            block_type=block_type,
            lines=tuple(lines),
            raw_text=raw_text,
        )
