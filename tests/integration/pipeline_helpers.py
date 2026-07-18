"""Helper functions for integration testing the end-to-end pipeline.

Purpose:
    Provide common setup, service instantiations, and orchestration functions
    to execute the complete Resume -> Match pipeline.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Mapping, Sequence

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
from ats_engine.domain.document_processing.canonical_models import CanonicalDocument

from ats_engine.domain.entity_extraction.section.service import SectionDetectionService
from ats_engine.domain.entity_extraction.contact.extractor import ContactInformationExtractor
from ats_engine.domain.entity_extraction.models import EntityExtractionContext, EntityCollection, EntityExtractionStatistics
from ats_engine.domain.entity_extraction.skills.service import SkillExtractionService
from ats_engine.domain.entity_extraction.experience.service import ExperienceExtractionService
from ats_engine.domain.entity_extraction.education.service import EducationExtractionService
from ats_engine.domain.entity_extraction.project.service import ProjectExtractionService
from ats_engine.domain.entity_extraction.certification.service import CertificationExtractionService
from ats_engine.domain.entity_extraction.canonical.service import CanonicalEntityCollectionService
from ats_engine.domain.entity_extraction.canonical.canonical_models import CanonicalEntityCollection

from ats_engine.domain.feature_engineering.service import FeatureEngineeringService
from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.feature_engineering.skills.extractor import SkillFeatureExtractor
from ats_engine.domain.feature_engineering.experience.extractor import ExperienceFeatureExtractor
from ats_engine.domain.feature_engineering.education.extractor import EducationFeatureExtractor
from ats_engine.domain.feature_engineering.project.extractor import ProjectFeatureExtractor
from ats_engine.domain.feature_engineering.certification.extractor import CertificationFeatureExtractor

from ats_engine.domain.matching.registry import FeatureMatcherRegistry
from ats_engine.domain.matching.service import MatchingService
from ats_engine.domain.matching.skill.matcher import SkillMatcher
from ats_engine.domain.matching.experience.matcher import ExperienceMatcher
from ats_engine.domain.matching.education.matcher import EducationMatcher
from ats_engine.domain.matching.project.matcher import ProjectMatcher
from ats_engine.domain.matching.certification.matcher import CertificationMatcher
from ats_engine.domain.matching.models import MatchCollection, CanonicalMatchCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules


def run_entity_extraction(resume_path: Path) -> CanonicalEntityCollection:
    """Run Document Ingestion and Entity Extraction on a resume file."""
    # 1. Parse
    registry = DocumentParserRegistry()
    registry.register("pdf", PdfDocumentParser)
    registry.register("docx", DocxDocumentParser)
    factory = DocumentParserFactory(registry)
    processing_service = DocumentProcessingService(factory)
    parsing_result = processing_service.parse(resume_path)

    # 2. Structural Analysis
    struct_rules = StructuralAnalysisRules()
    analyzer = StructuralAnalyzer(struct_rules)
    layout = analyzer.analyze(parsing_result.raw_document, parsing_result.normalized_document)

    # 3. Segmentation
    seg_rules = SegmentationRules()
    segmenter = DocumentSegmenter(seg_rules)
    segments = segmenter.segment(layout)

    # 4. Assemble Canonical Doc
    validation_rules = DocValidationRules()
    validation_service = DocumentValidationService(validation_rules)
    canonical_doc = validation_service.validate_and_assemble(
        raw_document=parsing_result.raw_document,
        normalized_document=parsing_result.normalized_document,
        document_layout=layout,
        segment_collection=segments,
        parser_used=parsing_result.metadata.parser_used,
    )

    # 5. Section Detection
    section_service = SectionDetectionService()
    sections = section_service.detect_sections(canonical_doc, {})

    # 6. Contact Extraction
    contact_extractor = ContactInformationExtractor()
    context = EntityExtractionContext(
        canonical_document=canonical_doc,
        correlation_id="integration_corr",
        rule_engine_config={},
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

    # 7. Extract skills, experience, education, projects, certifications
    skill_service = SkillExtractionService()
    skills = skill_service.extract_skills(canonical_doc, sections, {})

    experience_service = ExperienceExtractionService()
    experiences = experience_service.extract_experience(canonical_doc, sections, {})

    education_service = EducationExtractionService()
    education = education_service.extract_education(canonical_doc, sections, {})

    project_service = ProjectExtractionService()
    projects = project_service.extract_project(canonical_doc, sections, {})

    certification_service = CertificationExtractionService()
    certifications = certification_service.extract_certification(canonical_doc, sections, {})

    # 8. Assemble Canonical Collection
    canonical_collection_service = CanonicalEntityCollectionService()
    return canonical_collection_service.build(
        contacts=contacts,
        skills=skills,
        experiences=experiences,
        education=education,
        projects=projects,
        certifications=certifications,
        rule_engine_config={},
    )


def create_feature_service() -> FeatureEngineeringService:
    """Return a FeatureEngineeringService with all extractors registered."""
    service = FeatureEngineeringService()
    service.registry.register("skill", SkillFeatureExtractor)
    service.registry.register("experience", ExperienceFeatureExtractor)
    service.registry.register("education", EducationFeatureExtractor)
    service.registry.register("project", ProjectFeatureExtractor)
    service.registry.register("certification", CertificationFeatureExtractor)
    return service


def create_matching_service() -> MatchingService:
    """Return a MatchingService with all matchers registered."""
    registry = FeatureMatcherRegistry()
    registry.register("skill", SkillMatcher)
    registry.register("experience", ExperienceMatcher)
    registry.register("education", EducationMatcher)
    registry.register("project", ProjectMatcher)
    registry.register("certification", CertificationMatcher)
    return MatchingService(registry)


def run_full_pipeline(
    resume_path: Path,
    job_features: CanonicalFeatureCollection,
    matching_rules_payload: Mapping[str, Any] | None = None,
    canonical_rules: CanonicalMatchingRules | None = None,
) -> CanonicalMatchCollection:
    """Execute the entire E2E pipeline from resume file to CanonicalMatchCollection."""
    # Step 1: Entity Extraction
    entities = run_entity_extraction(resume_path)

    # Step 2: Feature Engineering
    feat_service = create_feature_service()
    
    skills_col = feat_service.extract_features(entities, ["skill"])
    exp_col = feat_service.extract_features(entities, ["experience"])
    edu_col = feat_service.extract_features(entities, ["education"])
    proj_col = feat_service.extract_features(entities, ["project"])
    cert_col = feat_service.extract_features(entities, ["certification"])

    from ats_engine.domain.feature_engineering.canonical.service import CanonicalFeatureCollectionService
    canon_service = CanonicalFeatureCollectionService()
    resume_features = canon_service.build(
        skill_features=skills_col,
        experience_features=exp_col,
        education_features=edu_col,
        project_features=proj_col,
        certification_features=cert_col,
    )

    # Step 3: Match individual categories
    match_service = create_matching_service()
    
    # We run the matcher for each category separately to get MatchCollections
    skill_col = match_service.match(resume_features, job_features, ["skill"], rules=matching_rules_payload)
    exp_col = match_service.match(resume_features, job_features, ["experience"], rules=matching_rules_payload)
    edu_col = match_service.match(resume_features, job_features, ["education"], rules=matching_rules_payload)
    proj_col = match_service.match(resume_features, job_features, ["project"], rules=matching_rules_payload)
    cert_col = match_service.match(resume_features, job_features, ["certification"], rules=matching_rules_payload)

    # Step 4: Canonical Match Collection Service
    canonical_match_service = CanonicalMatchCollectionService()
    return canonical_match_service.build(
        skill_matches=skill_col,
        experience_matches=exp_col,
        education_matches=edu_col,
        project_matches=proj_col,
        certification_matches=cert_col,
        rules=canonical_rules,
    )

