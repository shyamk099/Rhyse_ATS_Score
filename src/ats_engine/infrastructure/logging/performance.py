"""Performance timing hooks for execution duration logging.

Purpose:
    Provide context manager and decorator to measure and log execution duration.
"""

from __future__ import annotations

import time
import logging
from contextlib import contextmanager
from typing import Any, Generator


@contextmanager
def log_execution_time(
    logger: logging.Logger | logging.LoggerAdapter,
    operation_name: str,
    *,
    level: int = logging.INFO,
) -> Generator[None, None, None]:
    """Measure and log the execution time of a code block.

    Args:
        logger: Logger instance to output the time log.
        operation_name: Name of the operation being measured.
        level: Logging level (default INFO).
    """
    start_time = time.perf_counter()
    logger.log(level, "operation_started", extra={"operation": operation_name})
    try:
        yield
    finally:
        duration = time.perf_counter() - start_time
        logger.log(
            level,
            "operation_completed",
            extra={
                "operation": operation_name,
                "execution_time_seconds": duration,
                "execution_time_ms": duration * 1000.0,
            },
        )
