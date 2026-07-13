"""Unit tests for the Project Extraction engine.

Purpose:
    Verify compound entity assembly, URL provenance preservation, technology Skill ID
    integration, project name/role requirements, structured lists, canonical IDs,
    confidence calculation, and exception handling.
"""

from __future__ import annotations

import unittest

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
    SectionDetectionStatistics,
    SectionMetadata,
)
from ats_engine.domain.entity_extraction.project.project_models import ProjectCollection
from ats_engine.domain.entity_extraction.project.project_rules import ProjectExtractionRules
from ats_engine.domain.entity_extraction.project.service import ProjectExtractionService


class ProjectExtractionTests(unittest.TestCase):
    """Test suite validating compound project entity extraction."""

    def setUp(self) -> None:
        """Initialize the project extraction service."""
        self._service = ProjectExtractionService()

    def test_extracts_single_project_with_name_and_role(self) -> None:
        """Pipeline extracts a compound project with name, role, and dates."""
        text = "Portfolio Website Project\nSolo Developer\nSeptember 2022 - December 2022\n- Built personal website using React"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertIsInstance(collection, ProjectCollection)
        self.assertEqual(1, collection.statistics.total_projects)

        proj = collection.entities[0]
        self.assertTrue(proj.project_id.startswith("PROJ-"))
        self.assertEqual("Portfolio Website Project", proj.project_name)
        self.assertEqual("Solo Developer", proj.role)
        self.assertEqual("September 2022", proj.start_date_raw)
        self.assertEqual("December 2022", proj.end_date_raw)
        self.assertEqual(1, len(proj.responsibilities))

    def test_extracts_multiple_projects(self) -> None:
        """Pipeline extracts multiple independent project records."""
        doc, sections = self._create_document_and_sections([
            ("PROJECTS", "E-Commerce App\nLead Developer\n- Built shop cart"),
            ("PROJECTS", "Chat System\nSoftware Engineer\n- Developed sockets"),
        ])

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(2, collection.statistics.total_projects)
        self.assertEqual("PROJ-00000001", collection.entities[0].project_id)
        self.assertEqual("PROJ-00000002", collection.entities[1].project_id)

    def test_url_provenance_preservation(self) -> None:
        """Pipeline extracts repository and demo URLs with full provenance details."""
        text = "Search Engine Project\nDeveloper\nRepo: https://github.com/user/search-engine\nDemo: https://search-engine.vercel.app"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        proj = collection.entities[0]

        # Verify Repo URL
        self.assertIsNotNone(proj.repo_url)
        self.assertEqual("https://github.com/user/search-engine", proj.repo_url.original_value)
        self.assertEqual("https://github.com/user/search-engine", proj.repo_url.normalized_value)
        self.assertEqual("repository_domain_github.com", proj.repo_url.matched_rule)

        # Verify Demo URL
        self.assertIsNotNone(proj.demo_url)
        self.assertEqual("https://search-engine.vercel.app", proj.demo_url.original_value)
        self.assertEqual("https://search-engine.vercel.app", proj.demo_url.normalized_value)
        self.assertEqual("demo_domain_vercel.app", proj.demo_url.matched_rule)

    def test_technology_skill_id_integration(self) -> None:
        """Technologies resolve to canonical Skill IDs if mappings are provided."""
        text = "Web Crawler Project\n- Written in Python and TypeScript"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        rules = {
            "project_extraction_rules": {
                "technology_skill_mappings": {
                    "python": "SKL-00000001",
                    "typescript": "SKL-00000002",
                }
            }
        }

        collection = self._service.extract_project(doc, sections, rule_engine_config=rules)

        self.assertEqual(1, len(collection.entities))
        proj = collection.entities[0]

        # Verify Python resolved
        python_tech = next(t for t in proj.technologies if t.raw_name == "Python")
        self.assertEqual("SKL-00000001", python_tech.skill_id)

        # Verify TypeScript resolved
        ts_tech = next(t for t in proj.technologies if t.raw_name == "TypeScript")
        self.assertEqual("SKL-00000002", ts_tech.skill_id)

        # Verify Docker preserved raw (no skill ID)
        text_with_docker = "Container Project\n- Uses Docker"
        doc_docker, sections_docker = self._create_document_and_sections(
            [("PROJECTS", text_with_docker)]
        )
        collection_docker = self._service.extract_project(doc_docker, sections_docker, rule_engine_config=rules)
        proj_docker = collection_docker.entities[0]
        docker_tech = next(t for t in proj_docker.technologies if t.raw_name == "Docker")
        self.assertNull(docker_tech.skill_id) if hasattr(self, "assertNull") else self.assertIsNone(docker_tech.skill_id)

    def test_missing_project_name_falls_back_to_role(self) -> None:
        """Validator accepts project candidate if role is present but name is absent."""
        text = "https://example.com\nSolo Developer\n2022 - 2023\n- Built systems"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        proj = collection.entities[0]
        self.assertIsNone(proj.project_name)
        self.assertEqual("Solo Developer", proj.role)

    def test_missing_organization_gracefully(self) -> None:
        """Pipeline extracts project without organization field."""
        text = "Analytics Dashboard\n- Built widgets"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].organization)

    def test_missing_dates_gracefully(self) -> None:
        """Pipeline extracts project without dates."""
        text = "Database Engine\nLead Architect"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        self.assertIsNone(collection.entities[0].start_date_raw)

    def test_separates_responsibilities_and_achievements(self) -> None:
        """Project assembler groups bullets with metrics/verbs into achievements."""
        text = "Optimization Project\n- Maintained database index\n- Optimized query execution, reducing latency by 40%"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        proj = collection.entities[0]
        self.assertEqual(1, len(proj.responsibilities))
        self.assertEqual(1, len(proj.achievements))
        self.assertEqual("Maintained database index", proj.responsibilities[0])
        self.assertEqual("Optimized query execution, reducing latency by 40%", proj.achievements[0])

    def test_confidence_calculation(self) -> None:
        """Every project entity contains a scaled confidence score and reasons."""
        text = "E-Commerce App\nDeveloper at ShopCorp\nRepo: https://github.com/shop/app\n2022"
        doc, sections = self._create_document_and_sections(
            [("PROJECTS", text)]
        )

        collection = self._service.extract_project(doc, sections)

        self.assertEqual(1, len(collection.entities))
        proj = collection.entities[0]
        self.assertTrue(proj.confidence > 0.0)
        self.assertTrue(len(proj.matched_rules) > 0)
        self.assertIn("Matched rules:", proj.confidence_reason)

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

        sec_stats = SectionDetectionStatistics(
            section_counts={s: 1 for s, _ in section_texts},
            total_sections=len(sections_list),
            execution_duration_seconds=0.01,
        )
        sec_collection = SectionCollection(
            sections=tuple(sections_list),
            statistics=sec_stats,
        )
        return doc, sec_collection
