"""Common matching comparison helpers.

Purpose:
    Provide centralized string and dictionary exact matching comparison helpers
    reusable across domain-specific matching components.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def safe_compare_strings(str1: str | None, str2: str | None) -> bool:
    """Compare two optional string variables case-insensitively, stripping leading/trailing whitespace.

    Args:
        str1: First string.
        str2: Second string.

    Returns:
        True if they are equal after strip and lower, False otherwise.
    """
    if str1 is None or str2 is None:
        return False
    return str1.strip().lower() == str2.strip().lower()


def compare_matching_fields(
    val1: Mapping[str, Any],
    val2: Mapping[str, Any],
    fields: Sequence[str],
) -> bool:
    """Ensure all specified fields are present and safe_compare_strings is True for each of them.

    Args:
        val1: First value map.
        val2: Second value map.
        fields: Sequence of keys to compare.

    Returns:
        True if all fields match, False otherwise.
    """
    for f in fields:
        s1 = val1.get(f)
        s2 = val2.get(f)
        if not s1 or not s2:
            return False
        if not safe_compare_strings(str(s1), str(s2)):
            return False
    return True
