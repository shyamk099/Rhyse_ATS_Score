"""Unit tests for the Resume & Job Description Structural Analysis layer.

Purpose:
    Verify physical layout block partitioning, line classification, heading/list/table detection
    based on configurable rules, page tracking, and model immutability.
"""

from __future__ import annotations

import unittest
from typing import Sequence
from pydantic import ValidationError

from ats_engine.domain.document_processing.models import NormalizedDocument, RawDocument
from ats_engine.domain.document_processing.structure_models import BlockType, DocumentLayout
from ats_engine.domain.document_processing.structural_rules import StructuralAnalysisRules
from ats_engine.domain.document_processing.structural_analyzer import StructuralAnalyzer


class StructuralAnalysisTests(unittest.TestCase):
    """Test suite validating heuristics-based physical structure parsing."""

    def setUp(self) -> None:
        """Initialize analyzer with default rules."""
        self._rules = StructuralAnalysisRules()
        self._analyzer = StructuralAnalyzer(self._rules)

    def test_analyzes_paragraphs_and_headings(self) -> None:
        """Analyzer identifies headings and groups consecutive text lines into paragraphs."""
        content = (
            "CORE QUALIFICATIONS\n"
            "This is a standard paragraph line 1.\n"
            "This is a standard paragraph line 2.\n"
            "ANOTHER HEADING WITH NO PUNCTUATION"
        )
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=content,
            pages=(content,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=content,
            paragraph_count=2,
            line_count=4,
            char_count=len(content),
        )

        layout = self._analyzer.analyze(raw_doc, norm_doc)

        self.assertIsInstance(layout, DocumentLayout)
        self.assertEqual(3, layout.total_blocks)
        self.assertEqual(4, layout.total_lines)

        # Block 1: HEADING ("CORE QUALIFICATIONS")
        self.assertEqual(BlockType.HEADING, layout.blocks[0].block_type)
        self.assertEqual("CORE QUALIFICATIONS", layout.blocks[0].raw_text)

        # Block 2: TEXT (paragraphs grouped)
        self.assertEqual(BlockType.TEXT, layout.blocks[1].block_type)
        self.assertEqual(
            "This is a standard paragraph line 1.\nThis is a standard paragraph line 2.",
            layout.blocks[1].raw_text,
        )

        # Block 3: HEADING
        self.assertEqual(BlockType.HEADING, layout.blocks[2].block_type)

    def test_identifies_bullet_and_numbered_lists(self) -> None:
        """Analyzer classifies bullets and sequential numbering patterns as list blocks."""
        content = (
            "• Bullet list item 1\n"
            "- Bullet list item 2\n"
            "1. Numbered item 1\n"
            "A) Numbered item 2"
        )
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=content,
            pages=(content,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=content,
            paragraph_count=1,
            line_count=4,
            char_count=len(content),
        )

        layout = self._analyzer.analyze(raw_doc, norm_doc)

        # Consecutive list lines group into a single LIST block
        self.assertEqual(1, layout.total_blocks)
        self.assertEqual(BlockType.LIST, layout.blocks[0].block_type)
        self.assertEqual(4, len(layout.blocks[0].lines))

    def test_identifies_tables(self) -> None:
        """Analyzer flags lines containing custom column delimiters as tabular blocks."""
        content = (
            "Col1 | Col2 | Col3\n"
            "Val1 | Val2 | Val3"
        )
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=content,
            pages=(content,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=content,
            paragraph_count=1,
            line_count=2,
            char_count=len(content),
        )

        layout = self._analyzer.analyze(raw_doc, norm_doc)

        self.assertEqual(1, layout.total_blocks)
        self.assertEqual(BlockType.TABLE, layout.blocks[0].block_type)

    def test_respects_custom_heuristics_rules(self) -> None:
        """Custom structural rules modify heading length constraints and delimiters."""
        custom_rules = StructuralAnalysisRules(
            max_heading_length=10,  # Extremely short
            table_min_delimiters=1,
            table_delimiters=("\t",),
        )
        custom_analyzer = StructuralAnalyzer(custom_rules)

        content = (
            "VERY LONG HEADING TEXT THAT SHOULD EXCEED LIMIT\n"
            "Short\n"
            "Val1\tVal2"
        )
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=content,
            pages=(content,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=content,
            paragraph_count=1,
            line_count=3,
            char_count=len(content),
        )

        layout = custom_analyzer.analyze(raw_doc, norm_doc)

        # First line exceeds 10 chars, so it should classify as TEXT instead of HEADING
        self.assertEqual(BlockType.TEXT, layout.blocks[0].block_type)
        # Second line is short (<= 10 chars), so it classifies as HEADING
        self.assertEqual(BlockType.HEADING, layout.blocks[1].block_type)
        # Third line has a tab delimiter, matching the table config
        self.assertEqual(BlockType.TABLE, layout.blocks[2].block_type)

    def test_tracks_page_numbers_correctly(self) -> None:
        """Line mapping preserves 1-indexed page indices across page boundaries."""
        page1 = "Page 1 Line 1\nPage 1 Line 2"
        page2 = "Page 2 Line 1"
        
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=f"{page1}\n{page2}",
            pages=(page1, page2),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=f"{page1}\n{page2}",
            paragraph_count=2,
            line_count=3,
            char_count=len(page1) + len(page2) + 1,
        )

        layout = self._analyzer.analyze(raw_doc, norm_doc)

        self.assertEqual(3, layout.total_lines)
        
        # Verify lines are associated with correct page numbers
        self.assertEqual(1, layout.blocks[0].lines[0].page_number)
        self.assertEqual(1, layout.blocks[1].lines[0].page_number)
        self.assertEqual(2, layout.blocks[2].lines[0].page_number)

    def test_layout_models_are_immutable(self) -> None:
        """Caller cannot modify fields in structural blocks or lines."""
        content = "Line content"
        raw_doc = RawDocument(
            filename="doc.txt",
            file_size_bytes=100,
            raw_content=content,
            pages=(content,),
        )
        norm_doc = NormalizedDocument(
            cleaned_content=content,
            paragraph_count=1,
            line_count=1,
            char_count=len(content),
        )

        layout = self._analyzer.analyze(raw_doc, norm_doc)
        
        with self.assertRaises(ValidationError):
            layout.blocks[0].model_validate({"block_type": BlockType.TEXT})
