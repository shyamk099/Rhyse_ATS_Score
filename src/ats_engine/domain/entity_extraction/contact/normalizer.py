"""Contact information normalizer.

Purpose:
    Expose normalization routines to clean and standardize values (lowercasing emails, URL formatting).
"""

from __future__ import annotations

import re

from ats_engine.domain.entity_extraction.contact.exceptions import NormalizationError


class ContactNormalizer:
    """Stateless normalizer transforming contact values into canonical forms."""

    @classmethod
    def normalize(cls, value: str, entity_type: str) -> str:
        """Normalize extracted value based on its entity type.

        Args:
            value: The raw matched text.
            entity_type: Extracted type identifier.

        Returns:
            The normalized string representation.

        Raises:
            NormalizationError: If value normalization fails.
        """
        try:
            val = value.strip()
            etype = entity_type.lower()

            if etype == "email":
                return val.lower()

            if etype == "phone":
                # Preserve leading plus, strip spaces, dashes, dots, and parentheses
                is_intl = val.startswith("+")
                cleaned_digits = "".join(char for char in val if char.isdigit())
                return f"+{cleaned_digits}" if is_intl else cleaned_digits

            if etype in ("linkedin", "github", "portfolio"):
                normalized_url = val.lower()
                # Strip trailing slash if present
                if normalized_url.endswith("/"):
                    normalized_url = normalized_url[:-1]
                return normalized_url

            return val
        except Exception as error:
            raise NormalizationError(f"Failed to normalize contact value: {error}") from error
