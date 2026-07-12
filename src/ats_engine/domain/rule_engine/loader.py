"""Loader implementation for reading and parsing rule files.

Purpose:
    Scan rule directories, load YAML files, verify checksums, and instantiate rule envelopes.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

from ats_engine.domain.rule_engine.exceptions import RuleLoadError, RuleValidationError
from ats_engine.domain.rule_engine.models import RuleEnvelope, RuleMetadata
from ats_engine.domain.rule_engine.validator import RuleValidator


class RuleLoader:
    """Discovers, loads, and parses rule files from the file system."""

    @classmethod
    def load_from_directory(cls, directory_path: Path | str) -> list[RuleEnvelope]:
        """Scan a directory and load all YAML rule files.

        Args:
            directory_path: Absolute path to the rule directory.

        Returns:
            A list of successfully validated RuleEnvelope instances.

        Raises:
            RuleLoadError: If directory is missing, empty, contains invalid YAML, or file loading fails.
            RuleValidationError: If any loaded file fails validation rules.
        """
        dir_path = Path(directory_path)
        if not dir_path.is_dir():
            raise RuleLoadError(f"Rules directory not found or is not a directory: {dir_path}")

        yaml_files = list(dir_path.glob("*.yaml")) + list(dir_path.glob("*.yml"))
        if not yaml_files:
            raise RuleLoadError(f"No rule files (.yaml or .yml) found in directory: {dir_path}")

        envelopes: list[RuleEnvelope] = []
        for file_path in yaml_files:
            envelope = cls.load_from_file(file_path)
            envelopes.append(envelope)

        # Validate the aggregated rule set (e.g. for duplicates)
        RuleValidator.validate_rule_set(envelopes)
        return envelopes

    @classmethod
    def load_from_file(cls, file_path: Path) -> RuleEnvelope:
        """Parse a single rule file into a RuleEnvelope.

        Args:
            file_path: Absolute path to the rule file.

        Returns:
            A parsed, validated RuleEnvelope.
        """
        if not file_path.is_file():
            raise RuleLoadError(f"Rule file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as error:
            raise RuleLoadError(f"Failed to read rule file {file_path}: {error}") from error

        # Calculate SHA-256 checksum of raw content
        checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

        try:
            raw_data = yaml.safe_load(content)
        except Exception as error:
            raise RuleLoadError(f"Malformed YAML in rule file {file_path}: {error}") from error

        if not isinstance(raw_data, dict):
            raise RuleValidationError(f"Rule file {file_path} must define a root JSON object/dictionary.")

        # Ensure core fields are present before attempting model load
        if "metadata" not in raw_data:
            raise RuleValidationError(f"Rule file {file_path} is missing the required 'metadata' section.")
        if "payload" not in raw_data or not isinstance(raw_data["payload"], dict):
            raise RuleValidationError(f"Rule file {file_path} is missing the required 'payload' dict.")

        loaded_time = datetime.now(timezone.utc).isoformat()

        try:
            envelope = RuleEnvelope(
                metadata=RuleMetadata(**raw_data["metadata"]),
                checksum=checksum,
                source=file_path.name,
                loaded_timestamp=loaded_time,
                payload=raw_data["payload"],
            )
        except Exception as error:
            raise RuleValidationError(
                f"Validation failed for rule envelope {file_path.name}: {error}"
            ) from error

        # Validate single envelope rules
        RuleValidator.validate_envelope(envelope)
        return envelope
