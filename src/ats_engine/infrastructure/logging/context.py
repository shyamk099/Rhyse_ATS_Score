"""Thread-safe and async-safe context storage for generic logging metadata.

Purpose:
    Provide mechanism to store and retrieve arbitrary execution context key-value pairs.
"""

from __future__ import annotations

import contextvars
from typing import Any, Generator
from contextlib import contextmanager


class LoggingContext:
    """Thread-safe, async-safe context store for logging metadata."""

    _context: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar(
        "logging_context", default={}
    )

    @classmethod
    def get_all(cls) -> dict[str, Any]:
        """Return a copy of the current context dictionary."""
        return dict(cls._context.get())

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Return the value for a specific key in the current context."""
        return cls._context.get().get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a single key-value pair in the current context."""
        ctx = cls.get_all()
        ctx[key] = value
        cls._context.set(ctx)

    @classmethod
    def clear(cls) -> None:
        """Clear all keys in the current context."""
        cls._context.set({})

    @classmethod
    @contextmanager
    def context(cls, **kwargs: Any) -> Generator[None, None, None]:
        """Context manager to temporarily set metadata and restore previous state.

        Example:
            with LoggingContext.context(correlation_id="123", stage="parsing"):
                logger.info("Starting processing")
        """
        token = cls._context.set({**cls.get_all(), **kwargs})
        try:
            yield
        finally:
            cls._context.reset(token)
