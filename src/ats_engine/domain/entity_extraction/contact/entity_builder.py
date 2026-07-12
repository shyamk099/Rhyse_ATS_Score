"""Contact entity builder.

Purpose:
    Compile validated, normalized contact candidates into ExtractedEntity instances.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.contact.contact_candidate import ContactCandidate
from ats_engine.domain.entity_extraction.contact.contact_rules import ContactExtractionRules
from ats_engine.domain.entity_extraction.models import EntityLocation, ExtractedEntity


class ContactEntityBuilder:
    """Stateless builder wrapping candidates into Rhyse domain models."""

    @classmethod
    def build(
        cls,
        candidate: ContactCandidate,
        normalized_value: str,
        segment_id: str,
        rules: ContactExtractionRules,
    ) -> ExtractedEntity:
        """Create an ExtractedEntity instance from validated, normalized candidates.

        Args:
            candidate: Validated candidate details.
            normalized_value: Normalized value text.
            segment_id: The identifier of the parsed segment.
            rules: Configured rule guidelines containing confidence metrics.

        Returns:
            The compiled, immutable ExtractedEntity instance.
        """
        etype = candidate.entity_type
        
        # Determine deterministic confidence values from rule configs
        if etype == "email":
            confidence = rules.email_confidence
        elif etype == "phone":
            confidence = rules.phone_confidence
        elif etype == "linkedin":
            confidence = rules.linkedin_confidence
        elif etype == "github":
            confidence = rules.github_confidence
        elif etype == "portfolio":
            confidence = rules.portfolio_confidence
        else:
            confidence = 0.5

        location = EntityLocation(
            segment_id=segment_id,
            start_char=candidate.start_char,
            end_char=candidate.end_char,
        )

        return ExtractedEntity(
            entity_type=etype,
            value=normalized_value,
            confidence=confidence,
            location=location,
            metadata={"raw_value": candidate.value},
        )
