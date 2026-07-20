"""ScoreOrchestratorValidator definition.

Purpose:
    Provide stateless pre-flight validation of a ScoringRegistry before
    the orchestrator constructs an ExecutionPlan or delegates to the pipeline.
"""

from __future__ import annotations

from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.exceptions import RegistryValidationError


class ScoreOrchestratorValidator:
    """Stateless pre-flight registry validator for orchestration execution.

    Validates:
        1. Registry contains at least one scorer.
        2. All scorer classes are valid AbstractScorer subclasses.
        3. Enabled flags are boolean values.
        4. Enabled scorer priorities are unique (no ties).
        5. Execution order is deterministic (priorities form a strict total order).
    """

    @staticmethod
    def validate(registry: ScoringRegistry) -> None:
        """Run all pre-flight checks on the given registry.

        Args:
            registry: The ScoringRegistry to validate.

        Raises:
            RegistryValidationError: If any validation check fails.
        """
        names = registry.list()

        # 1. Non-empty check
        if not names:
            raise RegistryValidationError(
                "Registry validation failed: no scorers are registered. "
                "At least one scorer must be present for orchestration."
            )

        seen_priorities: dict[int, str] = {}

        for name in names:
            meta = registry.get_metadata(name)
            scorer_cls = registry.get(name)

            # 2. Valid AbstractScorer subclass
            if not (isinstance(scorer_cls, type) and issubclass(scorer_cls, AbstractScorer)):
                raise RegistryValidationError(
                    f"Registry validation failed: scorer '{name}' (type: {scorer_cls!r}) "
                    f"is not a valid AbstractScorer subclass."
                )

            # 3. Enabled flag is boolean
            enabled = meta.get("enabled")
            if not isinstance(enabled, bool):
                raise RegistryValidationError(
                    f"Registry validation failed: scorer '{name}' has an invalid 'enabled' "
                    f"flag value '{enabled}'. Must be True or False."
                )

            # 4 & 5. Priority uniqueness among enabled scorers
            if enabled:
                priority = meta.get("priority")
                if not isinstance(priority, int):
                    raise RegistryValidationError(
                        f"Registry validation failed: scorer '{name}' has a non-integer "
                        f"priority value '{priority}'."
                    )
                if priority in seen_priorities:
                    raise RegistryValidationError(
                        f"Registry validation failed: duplicate priority {priority} detected "
                        f"between scorers '{seen_priorities[priority]}' and '{name}'. "
                        "Execution order would be non-deterministic."
                    )
                seen_priorities[priority] = name
