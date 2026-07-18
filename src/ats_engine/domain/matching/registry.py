"""Feature Matcher registry.

Purpose:
    Maintain a thread-safe registry of FeatureMatcher classes available to the pipeline,
    permitting dynamic registrations.
"""

from __future__ import annotations

import threading
from typing import Sequence

from ats_engine.domain.matching.exceptions import MatcherRegistrationError, UnknownMatcherError
from ats_engine.domain.matching.matcher import FeatureMatcher


class FeatureMatcherRegistry:
    """Thread-safe registry mapping names to FeatureMatcher classes."""

    def __init__(self) -> None:
        """Initialize empty registry with mutex lock."""
        self._lock = threading.Lock()
        self._registry: dict[str, type[FeatureMatcher]] = {}

    def register(self, name: str, matcher_cls: type[FeatureMatcher]) -> None:
        """Register a new FeatureMatcher class coordinate.

        Args:
            name: Matcher identifier name.
            matcher_cls: Concrete subclass of FeatureMatcher.

        Raises:
            MatcherRegistrationError: If already registered or not a FeatureMatcher subclass.
        """
        if not issubclass(matcher_cls, FeatureMatcher):
            raise MatcherRegistrationError(
                f"Class '{matcher_cls.__name__}' is not a subclass of FeatureMatcher."
            )

        cleaned_name = name.strip()
        if not cleaned_name:
            raise MatcherRegistrationError("Matcher name cannot be empty or space-only.")

        with self._lock:
            if cleaned_name in self._registry:
                raise MatcherRegistrationError(
                    f"Matcher '{cleaned_name}' is already registered."
                )
            self._registry[cleaned_name] = matcher_cls

    def get(self, name: str) -> type[FeatureMatcher]:
        """Retrieve a registered FeatureMatcher class.

        Args:
            name: Identifier name.

        Returns:
            The registered FeatureMatcher class reference.

        Raises:
            UnknownMatcherError: If not found in the registry.
        """
        cleaned_name = name.strip()
        with self._lock:
            if cleaned_name not in self._registry:
                raise UnknownMatcherError(
                    f"Feature matcher '{cleaned_name}' is not registered."
                )
            return self._registry[cleaned_name]

    def list(self) -> list[str]:
        """List all currently registered matcher identifier keys.

        Returns:
            A list of registered keys.
        """
        with self._lock:
            return list(self._registry.keys())
