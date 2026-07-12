"""Unit tests for the Skill Extraction engine.

Purpose:
    Verify dictionary matching, overlap resolution (longest match wins), duplicate filters,
    scopes configurations, provenance recording, and confidence explainability reasons.
"""

from __future__ import annotations

import unittest
from typing import Sequence

from ats_engine.domain.document_processing.canonical_models import (
    CanonicalDocument,
    CanonicalMetadata,
    CanonicalStatistics,
)
from ats_engine.domain.document_processing.models import NormalizedDocument
from ats_engine.domain.document_processing.structure_models import (
    BlockType as LayoutBlockType,
    DocumentLayout,
    PhysicalBlock,
    PhysicalLine,
)
from ats_engine.domain.document_processing.segmentation_models import (
    DocumentSegment,
    SegmentCollection,
    SegmentMetadata,
)
from ats_engine.domain.entity_extraction.section.section_models import (
    Section,
    SectionCollection,
    SectionMetadata,
)
from ats_engine.domain.entity_extraction.skills.skill_models import SkillCollection
from ats_engine.domain.entity_extraction.skills.skill_rules import (
    SkillDefinition,
    SkillExtractionRules,
)
from ats_engine.domain.entity_extraction.skills.service import SkillExtractionService


class SkillExtractionTests(unittest.TestCase):
    """Test suite validating standard dictionary-based skill extraction."""

    def setUp(self) -> None:
        """Initialize the skill extraction service."""
        self._service = SkillExtractionService()

        # Set up a mock dictionary taxonomy for testing
        self._dictionary = {
            "SKILL-001": SkillDefinition(
                name="Python", aliases=["py", "python3"], category="programming_language"
            ),
            "SKILL-002": SkillDefinition(
                name="JavaScript", aliases=["js"], category="programming_language"
            ),
            "SKILL-003": SkillDefinition(
                name="Java", category="programming_language"
            ),
            "SKILL-004": SkillDefinition(
                name="Node.js", aliases=["nodejs", "node js"], category="runtime"
            ),
        }
        self._rules = SkillExtractionRules(dictionary=self._dictionary)

    def test_extracts_simple_skills_and_aliases(self) -> None:
        """Pipeline successfully extracts direct matches and alias synonyms."""
        text = "I write code in Python and JS."
        doc, sections = self._create_document_and_sections(
            [("SKILLS", text)]
        )

        collection = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": self._rules.model_dump()}
        )

        # Expected: 2 skills extracted (Python, JavaScript)
        self.assertEqual(2, len(collection.entities))
        
        py_skill = next(s for s in collection.entities if s.value == "Python")
        js_skill = next(s for s in collection.entities if s.value == "JavaScript")

        self.assertEqual("SKILL-001", py_skill.metadata["skill_id"])
        self.assertEqual("programming_language", py_skill.metadata["category"])
        self.assertEqual("Python", py_skill.metadata["matched_token"])
        
        self.assertEqual("SKILL-002", js_skill.metadata["skill_id"])
        self.assertEqual("JS", js_skill.metadata["matched_token"])
        self.assertEqual("js", js_skill.metadata["alias_matched"])

    def test_longest_match_wins_on_overlapping_spans(self) -> None:
        """DuplicateResolver filters out sub-spans when overlapping (JavaScript vs Java)."""
        text = "Experienced in JavaScript development."
        doc, sections = self._create_document_and_sections(
            [("SKILLS", text)]
        )

        collection = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": self._rules.model_dump()}
        )

        # "Java" is a substring of "JavaScript", but "JavaScript" is longer.
        # Expected: 1 skill (JavaScript), "Java" must be ignored.
        self.assertEqual(1, len(collection.entities))
        self.assertEqual("JavaScript", collection.entities[0].value)

    def test_respects_extraction_scope_filtering(self) -> None:
        """Pipeline only parses segments located in sections specified by scope rules."""
        # Skills in EXPERIENCE section, and skills in SKILLS section.
        doc, sections = self._create_document_and_sections(
            [
                ("EXPERIENCE", "Built a platform with Python."),
                ("SKILLS", "Programming: Java, Node.js"),
            ]
        )

        # Case 1: Scope is SKILLS only
        rules_skills_only = SkillExtractionRules(
            dictionary=self._dictionary,
            extraction_scope=["SKILLS"],
        )
        coll_skills = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": rules_skills_only.model_dump()}
        )
        # Expected: Java, Node.js (Python in EXPERIENCE is ignored)
        self.assertEqual(2, len(coll_skills.entities))
        self.assertNotIn("Python", [s.value for s in coll_skills.entities])

        # Case 2: Scope is EXPERIENCE and SKILLS
        rules_both = SkillExtractionRules(
            dictionary=self._dictionary,
            extraction_scope=["SKILLS", "EXPERIENCE"],
        )
        coll_both = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": rules_both.model_dump()}
        )
        # Expected: Python, Java, Node.js
        self.assertEqual(3, len(coll_both.entities))

    def test_handles_duplicate_strategies_accurately(self) -> None:
        """DuplicateResolver supports KEEP_HIGHEST_CONFIDENCE, KEEP_FIRST, and KEEP_ALL."""
        # Python occurs twice: first in EXPERIENCE, second in SKILLS section.
        doc, sections = self._create_document_and_sections(
            [
                ("EXPERIENCE", "Used Python for backend development."),
                ("SKILLS", "Keywords: Python, Java"),
            ]
        )

        # Case 1: KEEP_HIGHEST_CONFIDENCE
        # Confidence mapping: SKILLS is 1.0, EXPERIENCE is 0.8
        rules_highest = SkillExtractionRules(
            dictionary=self._dictionary,
            extraction_scope=["EXPERIENCE", "SKILLS"],
            duplicate_strategy="KEEP_HIGHEST_CONFIDENCE",
            confidence_mappings={"SKILLS": 1.0, "EXPERIENCE": 0.8},
        )
        coll_highest = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": rules_highest.model_dump()}
        )
        self.assertEqual(2, len(coll_highest.entities))
        py_highest = next(s for s in coll_highest.entities if s.value == "Python")
        # Python must have confidence 1.0 (from SKILLS)
        self.assertEqual(1.0, py_highest.confidence)

        # Case 2: KEEP_FIRST
        rules_first = SkillExtractionRules(
            dictionary=self._dictionary,
            extraction_scope=["EXPERIENCE", "SKILLS"],
            duplicate_strategy="KEEP_FIRST",
            confidence_mappings={"SKILLS": 1.0, "EXPERIENCE": 0.8},
        )
        coll_first = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": rules_first.model_dump()}
        )
        self.assertEqual(2, len(coll_first.entities))
        py_first = next(s for s in coll_first.entities if s.value == "Python")
        # Python must have confidence 0.8 (from EXPERIENCE, since it occurred first)
        self.assertEqual(0.8, py_first.confidence)

    def test_ignores_unregistered_skills_and_capitalization_differences(self) -> None:
        """Pipeline ignores terms not in the taxonomy dictionary and normalizes formatting variations."""
        text = "Skills: PyThOn, Node JS, C++"
        doc, sections = self._create_document_and_sections(
            [("SKILLS", text)]
        )

        collection = self._service.extract_skills(
            doc, 
            sections, 
            rule_engine_config={"skill_extraction_rules": self._rules.model_dump()}
        )

        # PyThOn normalizes to Python, Node JS normalizes to Node.js. C++ is unregistered.
        self.assertEqual(2, len(collection.entities))
        self.assertIn("Python", [s.value for s in collection.entities])
        self.assertIn("Node.js", [s.value for s in collection.entities])
        self.assertNotIn("C++", [s.value for s in collection.entities])

    def _create_document_and_sections(
        self, section_texts: list[tuple[str, str]]
    ) -> tuple[CanonicalDocument, SectionCollection]:
        blocks = []
        segments_list = []
        sections_list = []

        full_text_list = []
        block_idx = 1

        for stype, text in section_texts:
            full_text_list.append(text)
            
            line = PhysicalLine(
                text=text,
                line_number=block_idx,
                page_number=1,
                indentation_spaces=0,
                character_count=len(text),
            )
            block = PhysicalBlock(
                block_type=LayoutBlockType.TEXT,
                lines=(line,),
                raw_text=text,
            )
            blocks.append(block)

            metadata = SegmentMetadata(
                segment_id=f"segment_{block_idx:04d}",
                reading_order=block_idx,
                page_range=(1, 1),
                block_range=(block_idx, block_idx),
                character_count=len(text),
                line_count=1,
            )
            segment = DocumentSegment(
                segment_id=f"segment_{block_idx:04d}",
                text_content=text,
                metadata=metadata,
                associated_blocks=(block,),
            )
            segments_list.append(segment)

            sec_meta = SectionMetadata(
                section_type=stype,
                page_range=(1, 1),
                start_line=block_idx,
                end_line=block_idx,
                confidence=1.0,
                confidence_reason="Mock testing section setup",
            )
            section = Section(
                section_type=stype,
                text_content=text,
                metadata=sec_meta,
                associated_segments=(segment,),
            )
            sections_list.append(section)

            block_idx += 1

        full_text = "\n\n".join(full_text_list)
        norm_doc = NormalizedDocument(
            cleaned_content=full_text,
            paragraph_count=len(blocks),
            line_count=len(blocks),
            char_count=len(full_text),
        )
        layout = DocumentLayout(
            blocks=tuple(blocks),
            total_blocks=len(blocks),
            total_lines=len(blocks),
        )
        segments = SegmentCollection(
            segments=tuple(segments_list),
            total_segments=len(segments_list),
            total_characters=len(full_text),
        )
        meta = CanonicalMetadata(
            canonical_id="doc_123456",
            source_filename="test.pdf",
            file_size_bytes=100,
            page_count=1,
            parser_used="PdfDocumentParser",
            encoding="utf-8",
        )
        stats = CanonicalStatistics(
            total_characters=len(full_text),
            total_lines=len(blocks),
            total_paragraphs=len(blocks),
            total_segments=len(segments_list),
            total_blocks=len(blocks),
        )
        doc = CanonicalDocument(
            canonical_id="doc_123456",
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            metadata=meta,
            statistics=stats,
        )
        sec_collection = SectionCollection(
            sections=tuple(sections_list),
            statistics={"total_sections": len(sections_list), "execution_duration_seconds": 0.01},
        )
        return doc, sec_collection
