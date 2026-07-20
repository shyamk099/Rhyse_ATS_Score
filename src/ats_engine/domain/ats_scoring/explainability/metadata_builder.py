"""ExplainabilityMetadataBuilder definition.

Purpose:
    Compile explainability execution metadata.
"""

from __future__ import annotations

import datetime
from typing import Any


class ExplainabilityMetadataBuilder:
    """Builder generating metadata records for explainability executions."""

    @staticmethod
    def build(
        explainability_version: str = "1.0.0",
        pipeline_version: str = "1.0.0",
        framework_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """Create metadata dict."""
        now_str = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        return {
            "explainability_version": explainability_version,
            "pipeline_version": pipeline_version,
            "framework_version": framework_version,
            "timestamp": now_str,
        }
