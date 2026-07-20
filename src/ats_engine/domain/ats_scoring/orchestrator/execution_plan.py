"""ExecutionPlan definition.

Purpose:
    Provide a deterministic, immutable plan of scorers to be executed,
    sorted by priority (descending), with disabled scorers excluded.
"""

from __future__ import annotations

from typing import NamedTuple

from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.exceptions import ExecutionPlanError


class ExecutionPlanEntry(NamedTuple):
    """Immutable single-scorer entry within an ExecutionPlan.

    Attributes:
        name: The registered scorer name (e.g. "SKILL").
        scorer_cls: The AbstractScorer subclass type.
        priority: The numeric execution priority (higher = executes first).
    """

    name: str
    scorer_cls: type[AbstractScorer]
    priority: int


class ExecutionPlan:
    """Immutable, deterministic execution plan built from a ScoringRegistry.

    Responsibilities:
        - Obtain all scorers from the registry.
        - Sort enabled scorers by priority (descending — highest priority first).
        - Detect and raise ExecutionPlanError on duplicate priorities among enabled scorers.
        - Record skipped (disabled) scorer names.
        - Produce an immutable ordered sequence for deterministic execution.
    """

    __slots__ = ("_entries", "_skipped", "_registry_names")

    def __init__(
        self,
        entries: tuple[ExecutionPlanEntry, ...],
        skipped: tuple[str, ...],
        registry_names: tuple[str, ...],
    ) -> None:
        """Construct an ExecutionPlan (use ExecutionPlan.build() factory instead)."""
        self._entries = entries
        self._skipped = skipped
        self._registry_names = registry_names

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def entries(self) -> tuple[ExecutionPlanEntry, ...]:
        """Return the ordered, enabled scorer entries (descending priority)."""
        return self._entries

    @property
    def skipped(self) -> tuple[str, ...]:
        """Return names of scorers skipped because they are disabled."""
        return self._skipped

    @property
    def registry_names(self) -> tuple[str, ...]:
        """Return all registered scorer names regardless of enabled state."""
        return self._registry_names

    @property
    def execution_order(self) -> tuple[str, ...]:
        """Return scorer names in execution order."""
        return tuple(e.name for e in self._entries)

    def __len__(self) -> int:
        """Return the number of enabled scorers in this plan."""
        return len(self._entries)

    def __repr__(self) -> str:
        order = " → ".join(e.name for e in self._entries)
        return f"ExecutionPlan(order=[{order}], skipped={self._skipped})"

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @staticmethod
    def build(registry: ScoringRegistry) -> "ExecutionPlan":
        """Build a deterministic ExecutionPlan from the given registry.

        Args:
            registry: The ScoringRegistry containing scorer registrations.

        Returns:
            An immutable ExecutionPlan with entries sorted descending by priority.

        Raises:
            ExecutionPlanError: If no scorers are registered, or if duplicate
                priorities exist among enabled scorers.
        """
        names = registry.list()

        if not names:
            raise ExecutionPlanError(
                "ExecutionPlan cannot be built from an empty registry. "
                "At least one scorer must be registered."
            )

        enabled_entries: list[ExecutionPlanEntry] = []
        skipped: list[str] = []

        for name in names:
            meta = registry.get_metadata(name)
            scorer_cls = registry.get(name)
            is_enabled: bool = meta.get("enabled", True)
            priority: int = meta.get("priority", 100)

            if not is_enabled:
                skipped.append(name)
                continue

            enabled_entries.append(
                ExecutionPlanEntry(name=name, scorer_cls=scorer_cls, priority=priority)
            )

        # Detect duplicate priorities among enabled scorers
        seen_priorities: dict[int, str] = {}
        for entry in enabled_entries:
            if entry.priority in seen_priorities:
                raise ExecutionPlanError(
                    f"Duplicate priority {entry.priority} detected between scorers "
                    f"'{seen_priorities[entry.priority]}' and '{entry.name}'. "
                    "All enabled scorer priorities must be unique."
                )
            seen_priorities[entry.priority] = entry.name

        # Sort descending — highest priority executes first (consistent with ScoringPipeline)
        enabled_entries.sort(key=lambda e: e.priority, reverse=True)

        return ExecutionPlan(
            entries=tuple(enabled_entries),
            skipped=tuple(skipped),
            registry_names=tuple(names),
        )
