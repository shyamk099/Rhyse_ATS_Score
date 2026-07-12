"""Provider interface for accessing active rules.

Purpose:
    Define the interface for retrieving validated, active rule envelopes at runtime.
"""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from ats_engine.domain.rule_engine.models import RuleEnvelope


@runtime_checkable
class RuntimeRuleProvider(Protocol):
    """Protocol for rule retrieval and lookup operations at runtime."""

    def get(self, rule_id: str) -> RuleEnvelope:
        """Retrieve a specific rule envelope.

        Raises:
            RuleNotFoundError: If the rule does not exist.
        """
        ...

    def exists(self, rule_id: str) -> bool:
        """Check if a rule exists."""
        ...

    def list_all(self) -> Sequence[RuleEnvelope]:
        """List all currently active rules."""
        ...
