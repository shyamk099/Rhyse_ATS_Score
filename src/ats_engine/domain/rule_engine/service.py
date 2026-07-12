"""Service coordinating rule loading, caching, and retrieval operations.

Purpose:
    Expose the high-level, thread-safe public API for managing application business rules.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Sequence

from ats_engine.domain.rule_engine.cache import RuleCache
from ats_engine.domain.rule_engine.exceptions import RuleNotFoundError, RuleLoadError
from ats_engine.domain.rule_engine.loader import RuleLoader
from ats_engine.domain.rule_engine.models import RuleEnvelope
from ats_engine.domain.rule_engine.registry import RuleRegistry
from ats_engine.infrastructure.logging.factory import LoggerFactory


class RuleEngineService:
    """Entry point coordinating the loaded rule files, cache snapshots, and lookups."""

    def __init__(self, cache: RuleCache, logger: logging.Logger | None = None) -> None:
        """Initialize the rule engine service with its thread-safe cache."""
        self._cache = cache
        self._logger = logger or LoggerFactory.get_logger(__name__)
        self._last_loaded_directory: Path | None = None

    def load_rules(self, directory_path: Path | str) -> None:
        """Scan a directory, load and validate all YAML files, and update cache atomically.

        Args:
            directory_path: The directory path containing rule files.
        """
        dir_path = Path(directory_path)
        self._logger.info("rule_engine_loading_rules", extra={"directory": str(dir_path)})
        
        envelopes = RuleLoader.load_from_directory(dir_path)
        registry = RuleRegistry(envelopes)
        
        # Atomically swap cache reference
        self._cache.set(registry)
        self._last_loaded_directory = dir_path
        
        self._logger.info(
            "rule_engine_rules_loaded",
            extra={
                "directory": str(dir_path),
                "count": len(envelopes),
                "active_version": self.active_version(),
            },
        )

    def load(self, directory_path: Path | str) -> None:
        """Alias for load_rules."""
        self.load_rules(directory_path)

    def reload_rules(self) -> None:
        """Reload rules from the last successfully loaded directory path.

        Raises:
            RuleLoadError: If rules have not been previously loaded or reload fails.
        """
        if self._last_loaded_directory is None:
            raise RuleLoadError("No active rule set has been loaded yet; cannot reload.")
        self.load_rules(self._last_loaded_directory)

    def reload(self) -> None:
        """Alias for reload_rules."""
        self.reload_rules()

    def get(self, rule_id: str) -> RuleEnvelope:
        """Retrieve a specific active rule envelope.

        Args:
            rule_id: Unique identifier for the rule.

        Returns:
            The immutable RuleEnvelope.

        Raises:
            RuleNotFoundError: If the rule doesn't exist or service hasn't been loaded.
        """
        registry = self._cache.get()
        if registry is None:
            raise RuleNotFoundError("Rule engine has not loaded any rules yet.")
        
        envelope = registry.get(rule_id)
        if envelope is None:
            raise RuleNotFoundError(f"Rule with ID '{rule_id}' not found in active set.")
        return envelope

    def exists(self, rule_id: str) -> bool:
        """Check if a rule identifier exists in the active registry."""
        registry = self._cache.get()
        if registry is None:
            return False
        return registry.exists(rule_id)

    def list(self) -> Sequence[RuleEnvelope]:
        """List all currently active rule envelopes."""
        registry = self._cache.get()
        if registry is None:
            return []
        return registry.list_all()

    def active_version(self) -> str:
        """Return a compound version identifier representing the active rule set."""
        registry = self._cache.get()
        if registry is None:
            return "UNKNOWN"
        rules = registry.list_all()
        return ";".join(
            sorted(f"{r.metadata.rule_id}:{r.metadata.rule_version}" for r in rules)
        )

    def metadata(self) -> dict[str, dict[str, Any]]:
        """Return audit metadata summaries for all active rules."""
        registry = self._cache.get()
        if registry is None:
            return {}
        return {
            env.metadata.rule_id: {
                "rule_version": env.metadata.rule_version,
                "effective_date": env.metadata.effective_date,
                "status": env.metadata.status,
                "checksum": env.metadata.checksum if hasattr(env.metadata, 'checksum') else env.checksum,
                "source": env.source,
                "loaded_timestamp": env.loaded_timestamp,
            }
            for env in registry.list_all()
        }
