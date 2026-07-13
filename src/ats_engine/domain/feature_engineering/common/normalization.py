"""Shared text normalization utilities for Book 04 Feature Engineering.

Purpose:
    Provide consistent structural whitespace normalization (trim margins,
    collapse duplicate spaces) without altering raw canonical names.
"""

from __future__ import annotations

import re


def normalize_text(text: str | None) -> str | None:
    """Trim whitespace and collapse duplicate spaces inside a string.

    Args:
        text: Source string.

    Returns:
        Cleaned string or None if input was None.
    """
    if text is None:
        return None
    # Collapse multiple spaces into a single space, trim margins
    return re.sub(r"\s+", " ", text).strip()
