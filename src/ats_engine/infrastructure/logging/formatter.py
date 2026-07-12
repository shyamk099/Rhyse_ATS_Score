"""Structured formatter for formatting python logs as JSON.

Purpose:
    Provide consistent JSON formatting for all log records, including exceptions and context.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from ats_engine.infrastructure.logging.context import LoggingContext


class StructuredFormatter(logging.Formatter):
    """Format log records into structured, queryable JSON strings."""

    def __init__(self, *, include_context: bool = True) -> None:
        """Initialize the formatter.

        Args:
            include_context: Whether to automatically merge active LoggingContext variables.
        """
        super().__init__()
        self._include_context = include_context

    def format(self, record: logging.LogRecord) -> str:
        """Convert a LogRecord into a JSON string."""
        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include standard logging fields
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            log_data["stack_info"] = self.formatStack(record.stack_info)

        # Merge active LoggingContext if enabled
        if self._include_context:
            context = LoggingContext.get_all()
            if context:
                log_data["context"] = context

        # Merge any 'extra' fields passed to the logger
        # Standard LogRecord fields are excluded from extra
        reserved = {
            "args", "asctime", "created", "exc_info", "exc_text", "filename",
            "funcName", "levelname", "levelno", "lineno", "module", "msecs",
            "message", "msg", "name", "pathname", "process", "processName",
            "relativeCreated", "stack_info", "thread", "threadName"
        }
        
        extra_data = {k: v for k, v in record.__dict__.items() if k not in reserved and not k.startswith("_")}
        if extra_data:
            log_data["extra"] = extra_data

        return json.dumps(log_data)
