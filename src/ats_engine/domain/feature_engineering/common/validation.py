"""Shared validation checks for Book 04 Feature Engineering.

Purpose:
    Provide unified required field checking and confidence bounds evaluation.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def validate_required_fields(
    entity_val: Any,
    entity_metadata: Mapping[str, Any],
    required: Sequence[str],
    field_mappings: Mapping[str, str] | None = None,
) -> None:
    """Ensure required fields are present and non-empty.

    Args:
        entity_val: Default value property of the entity.
        entity_metadata: Metadata mapping carrying custom values.
        required: Sequence of required keys.
        field_mappings: Mapping translating config required key to entity attributes.

    Raises:
        ValueError: If a required field is missing or empty.
    """
    for req in required:
        # Check mapping or default check
        target_name = field_mappings.get(req, req) if field_mappings else req
        if target_name == "value" or target_name == "name":
            if not isinstance(entity_val, str) or not entity_val.strip():
                raise ValueError(f"Required feature field '{req}' is empty or missing.")
        else:
            val = entity_metadata.get(target_name)
            if val is None or (isinstance(val, str) and not val.strip()):
                raise ValueError(f"Required feature metadata field '{req}' is empty or missing.")


def validate_confidence_threshold(
    confidence: float,
    threshold: float,
) -> None:
    """Assert confidence is equal to or greater than rules threshold limit.

    Args:
        confidence: Evaluated confidence score.
        threshold: Configured lower boundary limit.

    Raises:
        ValueError: If confidence is lower than threshold.
    """
    if confidence < threshold:
        raise ValueError(
            f"Confidence score {confidence} falls below "
            f"configured boundary threshold of {threshold}."
        )
