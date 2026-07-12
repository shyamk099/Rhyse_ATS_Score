"""Logging context adapter.

Purpose:
    Wrap loggers to automatically merge current thread-safe LoggingContext into extra fields.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping


class LoggingContextAdapter(logging.LoggerAdapter):
    """LoggerAdapter that merges thread-safe LoggingContext into LogRecord extras."""

    def __init__(self, logger: logging.Logger, extra: Mapping[str, Any] | None = None) -> None:
        """Initialize the adapter with a logger and optional default extra fields."""
        super().__init__(logger, extra or {})

    def process(self, msg: Any, kwargs: Any) -> tuple[Any, Any]:
        """Inject context and extra fields into the keyword arguments."""
        # Ensure extra dictionary exists in kwargs
        kwargs_extra = kwargs.setdefault("extra", {})
        
        # Merge adapter defaults
        if self.extra:
            for k, v in self.extra.items():
                kwargs_extra.setdefault(k, v)

        return msg, kwargs
