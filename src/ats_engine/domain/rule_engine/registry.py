"""Registry of active, validated rule envelopes.

Purpose:
    Hold the map of loaded rule envelopes and support basic existence/retrieval operations.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from ats_engine.domain.rule_engine.models import RuleEnvelope


class RuleRegistry:
    """Registry managing an immutable snapshot of rule envelopes."""

    def __init__(self, envelopes: Sequence[RuleEnvelope]) -> None:
        """Initialize registry with a sequence of validated envelopes."""
        self._envelopes: Mapping[str, RuleEnvelope] = {
            env.metadata.rule_id: env for env in envelopes
        }

    def get(self, rule_id: str) -> RuleEnvelope | None:
        """Retrieve a rule envelope by identifier."""
        return self._envelopes.get(rule_id)

    def exists(self, rule_id: str) -> bool:
        """Check if a rule envelope exists under an identifier."""
        return rule_id in self._envelopes

    def list_all(self) -> list[RuleEnvelope]:
        """Return a list of all registered rule envelopes."""
        return list(self._envelopes.values())
