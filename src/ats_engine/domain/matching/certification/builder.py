"""MatchResult builder for Certification features.

Purpose:
    Compile validated candidate matches into immutable MatchResult DTOs.
"""

from __future__ import annotations

import datetime
from typing import Any

from ats_engine.domain.feature_engineering.models import FeatureProvenance
from ats_engine.domain.matching.models import MatchLocation, MatchMetadata, MatchResult
from ats_engine.domain.matching.certification.candidate_builder import CertificationMatchCandidate


class CertificationMatchBuilder:
    """Builder producing immutable MatchResult DTOs from Certification candidates."""

    @classmethod
    def build(
        cls,
        candidate: CertificationMatchCandidate,
        context: Any,
    ) -> MatchResult:
        """Construct the MatchResult output DTO."""
        rf = candidate.resume_feature
        jf = candidate.job_feature

        location = MatchLocation(
            resume_feature_location=rf.locations[0] if rf.locations else None,
            job_feature_location=jf.locations[0] if jf.locations else None,
            resume_page=rf.locations[0].page_number if rf.locations and rf.locations[0].page_number else None,
            job_page=jf.locations[0].page_number if jf.locations and jf.locations[0].page_number else None,
            resume_source_ids=(rf.provenance.source_entity_id,) if rf.provenance.source_entity_id else (),
            job_source_ids=(jf.provenance.source_entity_id,) if jf.provenance.source_entity_id else (),
        )

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

        meta = MatchMetadata(
            correlation_id=context.correlation_id,
            matcher_type="CertificationMatcher",
            execution_timestamp=now_utc,
            rules_version=context.execution_metadata.get("rules_version", "matching_rules_v1.0"),
            custom_attributes={
                "resume_certification_name": rf.value.get("certification_name"),
                "job_certification_name": jf.value.get("certification_name"),
                "resume_issuing_org": rf.value.get("issuing_organization"),
                "job_issuing_org": jf.value.get("issuing_organization"),
            },
        )

        provenance = FeatureProvenance(
            source_entity_id=rf.provenance.source_entity_id,
            source_entity_type="CERTIFICATION",
            source_section=rf.provenance.source_section,
            source_document=rf.provenance.source_document,
            matched_rules=tuple(
                set(rf.provenance.matched_rules + jf.provenance.matched_rules)
            ),
        )

        return MatchResult(
            match_id=f"MATCH-CERT-{rf.feature_id}-{jf.feature_id}",
            matcher_type="CertificationMatcher",
            resume_feature_id=rf.feature_id,
            job_feature_id=jf.feature_id,
            metadata=meta,
            provenance=provenance,
            locations=location,
        )
