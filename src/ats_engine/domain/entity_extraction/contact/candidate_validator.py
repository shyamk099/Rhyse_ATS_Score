"""Contact candidate validator.

Purpose:
    Perform sanity checks on email structures, phone digit lengths, and URL formats.
"""

from __future__ import annotations

from ats_engine.domain.entity_extraction.contact.contact_candidate import ContactCandidate


class CandidateValidator:
    """Stateless validator auditing intermediate candidate string alignments."""

    @classmethod
    def validate_candidate(cls, candidate: ContactCandidate) -> bool:
        """Validate candidate formatting.

        Args:
            candidate: Discovered candidate.

        Returns:
            True if candidate satisfies format rules, False otherwise.
        """
        val = candidate.value.strip()
        etype = candidate.entity_type

        if etype == "email":
            if "@" not in val or "." not in val:
                return False
            parts = val.split("@")
            if len(parts) != 2 or not parts[0] or not parts[1]:
                return False
            if "." not in parts[1]:
                return False

        elif etype == "phone":
            digits = "".join(char for char in val if char.isdigit())
            # Sanity bounds: typically between 7 and 20 digits
            if len(digits) < 7 or len(digits) > 20:
                return False

        elif etype in ("linkedin", "github", "portfolio"):
            if len(val) < 5 or len(val) > 255:
                return False
            if etype == "portfolio" and "." not in val:
                return False

        return True
