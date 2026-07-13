"""Duplicate resolver.

Purpose:
    Deduplicate and resolve duplicate entities deterministically based on
    Rule Engine policies.
"""

from __future__ import annotations

from typing import Sequence, TypeVar, Any
from pydantic import BaseModel

from ats_engine.domain.entity_extraction.canonical.canonical_rules import CanonicalValidationRules

T = TypeVar("T", bound=BaseModel)


class DuplicateResolver:
    """Stateless resolver deduplicating entities based on configurable strategies."""

    @classmethod
    def resolve(
        cls,
        entities: Sequence[T],
        rules: CanonicalValidationRules,
        key_field: str = "experience_id",
    ) -> Sequence[T]:
        """Deduplicate entities using configured strategy.

        Args:
            entities: Sequence of entities to check.
            rules: Configuration rules.
            key_field: The unique ID field name for tracking.

        Returns:
            Deduplicated sequence of entities.
        """
        if not entities:
            return entities

        seen_keys: dict[str, T] = {}

        for ent in entities:
            key_val = getattr(ent, key_field, None)
            if not key_val:
                continue

            if key_val in seen_keys:
                existing = seen_keys[key_val]
                
                # Check duplicate strategy
                if rules.duplicate_strategy == "KEEP_HIGHEST_CONFIDENCE":
                    conf_exist = getattr(existing, "confidence", 0.0)
                    conf_new = getattr(ent, "confidence", 0.0)
                    if conf_new > conf_exist:
                        seen_keys[key_val] = ent
                elif rules.duplicate_strategy == "KEEP_FIRST":
                    # Do nothing, keep existing
                    pass
                else:
                    # Default: keep highest confidence
                    conf_exist = getattr(existing, "confidence", 0.0)
                    conf_new = getattr(ent, "confidence", 0.0)
                    if conf_new > conf_exist:
                        seen_keys[key_val] = ent
            else:
                seen_keys[key_val] = ent

        return tuple(seen_keys.values())
