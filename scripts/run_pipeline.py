"""End-to-End Validation Runner for the ATS Resume Intelligence Engine.

Purpose:
    Execute the entire ingestion-to-extraction pipeline on a sample resume,
    generating outputs under output/ and a readable markdown summary.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add src folder to PYTHONPATH to make script self-contained
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import json
import os
import time
import traceback
from typing import Any, Dict

from ats_engine.application.composition_root import CompositionRoot
from ats_engine.domain.document_processing.docx_parser import DocxDocumentParser
from ats_engine.domain.document_processing.factory import DocumentParserFactory
from ats_engine.domain.document_processing.pdf_parser import PdfDocumentParser
from ats_engine.domain.document_processing.registry import DocumentParserRegistry
from ats_engine.domain.document_processing.service import DocumentProcessingService
from ats_engine.domain.document_processing.structural_analyzer import StructuralAnalyzer
from ats_engine.domain.document_processing.structural_rules import StructuralAnalysisRules
from ats_engine.domain.document_processing.segmenter import DocumentSegmenter
from ats_engine.domain.document_processing.segmentation_rules import SegmentationRules
from ats_engine.domain.document_processing.validation_service import DocumentValidationService
from ats_engine.domain.document_processing.canonical_rules import CanonicalValidationRules as DocValidationRules
from ats_engine.domain.entity_extraction.section.service import SectionDetectionService
from ats_engine.domain.entity_extraction.contact.extractor import ContactInformationExtractor
from ats_engine.domain.entity_extraction.models import EntityExtractionContext, EntityCollection, EntityExtractionStatistics
from ats_engine.domain.entity_extraction.skills.service import SkillExtractionService
from ats_engine.domain.entity_extraction.experience.service import ExperienceExtractionService
from ats_engine.domain.entity_extraction.education.service import EducationExtractionService
from ats_engine.domain.entity_extraction.project.service import ProjectExtractionService
from ats_engine.domain.entity_extraction.certification.service import CertificationExtractionService
from ats_engine.domain.entity_extraction.canonical.service import CanonicalEntityCollectionService


def main() -> None:
    """Main execution path for run_pipeline CLI utility."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_pipeline.py <path_to_resume>")
        sys.exit(1)

    resume_path = Path(sys.argv[1])
    if not resume_path.is_file():
        print(f"Error: file not found: {resume_path}")
        sys.exit(1)

    print(f"Starting E2E validation pipeline runner on: {resume_path.name}")
    start_time_perf = time.perf_counter()
    start_time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Initialize composition root and logger/rules
    print("Stage 1: Initializing composition root and loading rules...")
    root = CompositionRoot()
    logger = root.rule_engine_service._logger
    rules_service = root.rule_engine_service

    # Retrieve loaded config rules payloads if present
    rule_config: Dict[str, Any] = {}
    if rules_service.exists("parser_rules"):
        parser_payload = rules_service.get("parser_rules").payload
        if parser_payload:
            rule_config = parser_payload

    try:
        # 2. Document Parsing
        print("Stage 2: Parsing document...")
        logger.info("runner_parsing_start")
        registry = DocumentParserRegistry()
        registry.register("pdf", PdfDocumentParser)
        registry.register("docx", DocxDocumentParser)
        factory = DocumentParserFactory(registry)
        processing_service = DocumentProcessingService(factory)
        
        parsing_result = processing_service.parse(resume_path)
        raw_doc = parsing_result.raw_document
        norm_doc = parsing_result.normalized_document
        logger.info("runner_parsing_success")

        # 3. Structural Analysis
        print("Stage 3: Analyzing physical layout...")
        logger.info("runner_structural_analysis_start")
        struct_rules = StructuralAnalysisRules()
        analyzer = StructuralAnalyzer(struct_rules)
        layout = analyzer.analyze(raw_doc, norm_doc)
        logger.info("runner_structural_analysis_success")

        # 4. Segmentation & Reading Order
        print("Stage 4: Segmenting document and resolving reading order...")
        logger.info("runner_segmentation_start")
        seg_rules = SegmentationRules()
        segmenter = DocumentSegmenter(seg_rules)
        segments = segmenter.segment(layout)
        logger.info("runner_segmentation_success")

        # 5. Canonical Document Assembly
        print("Stage 5: Validating and assembling CanonicalDocument...")
        logger.info("runner_canonical_assembly_start")
        validation_rules = DocValidationRules()
        validation_service = DocumentValidationService(validation_rules)
        canonical_doc = validation_service.validate_and_assemble(
            raw_document=raw_doc,
            normalized_document=norm_doc,
            document_layout=layout,
            segment_collection=segments,
            parser_used=parsing_result.metadata.parser_used,
        )
        logger.info("runner_canonical_assembly_success")

        # 6. Section Detection
        print("Stage 6: Detecting sections...")
        logger.info("runner_section_detection_start")
        section_service = SectionDetectionService()
        sections = section_service.detect_sections(canonical_doc, rule_config)
        logger.info("runner_section_detection_success")

        # 7. Contact Extraction
        print("Stage 7: Extracting contact details...")
        logger.info("runner_contact_extraction_start")
        contact_extractor = ContactInformationExtractor()
        context = EntityExtractionContext(
            canonical_document=canonical_doc,
            correlation_id="runner_corr",
            rule_engine_config=rule_config,
        )
        contacts_list = []
        for seg in canonical_doc.segment_collection.segments:
            contacts_list.extend(contact_extractor.extract(seg, context))
        contacts = EntityCollection(
            entities=tuple(contacts_list),
            statistics=EntityExtractionStatistics(
                extractor_counts={"contact": len(contacts_list)},
                total_entities=len(contacts_list),
                execution_duration_seconds=0.01,
            ),
        )
        logger.info("runner_contact_extraction_success")

        # 8. Skill Extraction
        print("Stage 8: Extracting skills...")
        logger.info("runner_skill_extraction_start")
        skill_service = SkillExtractionService()
        skills = skill_service.extract_skills(canonical_doc, sections, rule_config)
        logger.info("runner_skill_extraction_success")

        # 9. Experience Extraction
        print("Stage 9: Extracting experience...")
        logger.info("runner_experience_extraction_start")
        experience_service = ExperienceExtractionService()
        experiences = experience_service.extract_experience(canonical_doc, sections, rule_config)
        logger.info("runner_experience_extraction_success")

        # 10. Education Extraction
        print("Stage 10: Extracting education...")
        logger.info("runner_education_extraction_start")
        education_service = EducationExtractionService()
        education = education_service.extract_education(canonical_doc, sections, rule_config)
        logger.info("runner_education_extraction_success")

        # 11. Project Extraction
        print("Stage 11: Extracting projects...")
        logger.info("runner_project_extraction_start")
        project_service = ProjectExtractionService()
        projects = project_service.extract_project(canonical_doc, sections, rule_config)
        logger.info("runner_project_extraction_success")

        # 12. Certification Extraction
        print("Stage 12: Extracting certifications...")
        logger.info("runner_certification_extraction_start")
        certification_service = CertificationExtractionService()
        certifications = certification_service.extract_certification(canonical_doc, sections, rule_config)
        logger.info("runner_certification_extraction_success")

        # 13. Canonical Collection and Validation
        print("Stage 13: Assembling and validating CanonicalEntityCollection...")
        logger.info("runner_canonical_collection_start")
        canonical_collection_service = CanonicalEntityCollectionService()
        canonical_collection = canonical_collection_service.build(
            contacts=contacts,
            skills=skills,
            experiences=experiences,
            education=education,
            projects=projects,
            certifications=certifications,
            rule_engine_config=rule_config,
        )
        logger.info("runner_canonical_collection_success")

    except Exception as exc:
        print("\n!!! PIPELINE RUNNER EXCEPTION ENCOUNTERED !!!")
        print(f"Failed Stage: {sys.exc_info()[2].tb_next.tb_frame.f_code.co_name if sys.exc_info()[2] and sys.exc_info()[2].tb_next else 'Initialization'}")
        print(f"Exception Type: {exc.__class__.__name__}")
        print(f"Message: {exc}")
        print("\nStack Trace:")
        traceback.print_exc()
        sys.exit(1)

    duration = time.perf_counter() - start_time_perf
    end_time_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    # Write Pretty JSON Outputs
    def _write_json(filename: str, model_data: Any) -> None:
        filepath = output_dir / filename
        data = model_data.model_dump() if hasattr(model_data, "model_dump") else model_data
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    _write_json("canonical_document.json", canonical_doc)
    _write_json("sections.json", sections)
    _write_json("contacts.json", contacts)
    _write_json("skills.json", skills)
    _write_json("experience.json", experiences)
    _write_json("education.json", education)
    _write_json("projects.json", projects)
    _write_json("certifications.json", certifications)
    _write_json("canonical_entity_collection.json", canonical_collection)
    _write_json("validation_summary.json", canonical_collection.validation_summary)

    # Compile Markdown Summary
    summary_md = f"""# ATS Resume Intelligence Engine
## Pipeline Execution Summary

---

### Input File
- **Filename**: `{resume_path.name}`

---

### Document Processing
- **Status**: `SUCCESS`
- **Pages**: `{canonical_doc.metadata.page_count}`
- **Characters**: `{canonical_doc.statistics.total_characters}`
- **Segments**: `{canonical_doc.statistics.total_segments}`

---

### Entity Extraction
- **Sections**: `{sections.statistics.total_sections}`
- **Contacts**: `{len(contacts.entities)}`
- **Skills**: `{skills.statistics.total_skills_found}`
- **Experience**: `{experiences.statistics.total_experiences}`
- **Education**: `{education.statistics.total_education_records}`
- **Projects**: `{projects.statistics.total_projects}`
- **Certifications**: `{certifications.statistics.total_certifications}`

---

### Canonical Collection
- **Validation Status**: `{canonical_collection.validation_summary.status}`
- **Warnings**: `{len(canonical_collection.validation_summary.warnings)}`
- **Errors**: `{len(canonical_collection.validation_summary.errors)}`
- **Duplicate Entities**: `{canonical_collection.validation_summary.duplicate_count}`
- **Broken References**: `{canonical_collection.validation_summary.reference_errors}`

---

### Execution Details
- **Start Time**: `{start_time_str}`
- **End Time**: `{end_time_str}`
- **Total Duration**: `{duration:.4f} seconds`
"""

    with open(output_dir / "pipeline_summary.md", "w", encoding="utf-8") as f:
        f.write(summary_md)

    print("\n--- Pipeline Summary Output ---")
    print(summary_md)
    print("-------------------------------")
    print(f"Pipeline executed successfully. Outputs stored under output/")


if __name__ == "__main__":
    main()
