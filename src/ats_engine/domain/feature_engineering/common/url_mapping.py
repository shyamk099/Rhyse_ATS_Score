"""Shared serialization utilities for custom URL objects.

Purpose:
    Provide consistent serialization mapping for custom ProjectURL and CertificationURL objects
    to ensure they can be stored generically without domain class dependencies.
"""

from __future__ import annotations

from typing import Any


def map_custom_url(url_obj: Any) -> dict[str, str] | None:
    """Map dynamic custom URL objects to a dictionary representation.

    Args:
        url_obj: Custom URL model (ProjectURL, CertificationURL).

    Returns:
        A dictionary representation or None if input was None.
    """
    if url_obj is None:
        return None

    # Handle standard dynamic Pydantic attributes or raise fallback
    original_value = getattr(url_obj, "original_value", "")
    normalized_value = getattr(url_obj, "normalized_value", "")
    matched_rule = getattr(url_obj, "matched_rule", "")

    return {
        "original_value": original_value,
        "normalized_value": normalized_value,
        "matched_rule": matched_rule,
    }
