"""Validation rules for rule engine files.

Purpose:
    Enforce schema correctness, version compliance, and prevent duplicate rule identifiers.
"""

from __future__ import annotations

import re
from typing import Sequence

from ats_engine.domain.rule_engine.exceptions import DuplicateRuleError, RuleValidationError
from ats_engine.domain.rule_engine.models import RuleEnvelope


class RuleValidator:
    """Validator for rule envelopes and rule collections."""

    _ID_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")

    @classmethod
    def validate_envelope(cls, envelope: RuleEnvelope) -> None:
        """Validate a single rule envelope.

        Raises:
            RuleValidationError: If properties of the envelope are invalid.
        """
        metadata = envelope.metadata
        
        # Validate identifier characters
        if not cls._ID_PATTERN.match(metadata.rule_id):
            raise RuleValidationError(
                f"Invalid rule identifier: '{metadata.rule_id}'. Must be alphanumeric and underscores only."
            )

        # Validate version pattern (must be simple semver e.g. x.y.z or major.minor)
        if not re.match(r"^\d+(\.\d+)*$", metadata.rule_version):
            raise RuleValidationError(
                f"Invalid version format: '{metadata.rule_version}' for rule '{metadata.rule_id}'."
            )

    @classmethod
    def validate_rule_set(cls, envelopes: Sequence[RuleEnvelope]) -> None:
        """Validate a collection of rules for consistency.

        Raises:
            DuplicateRuleError: If duplicate rule_ids are present in the collection.
            RuleValidationError: If any individual envelope validation fails.
        """
        seen_ids: set[str] = set()
        for envelope in envelopes:
            cls.validate_envelope(envelope)
            
            rule_id = envelope.metadata.rule_id
            if rule_id in seen_ids:
                raise DuplicateRuleError(f"Duplicate rule identifier detected: '{rule_id}'")
            seen_ids.add(rule_id)
