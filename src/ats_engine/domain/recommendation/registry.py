"""RecommendationRegistry definition.

Purpose:
    Manage registration and deterministic ordering of BaseRecommendationProvider
    instances. Mirrors ScoringRegistry from Book 06.
"""

from __future__ import annotations

import logging
from typing import Any

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError
from ats_engine.infrastructure.logging.factory import LoggerFactory


class RecommendationRegistry:
    """Registry managing the lifecycle and ordering of recommendation providers.

    Responsibilities:
        - Register provider instances with unique names.
        - Detect duplicate registrations.
        - Provide deterministic iteration order sorted by provider priority.
        - Lookup individual providers by name.
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._providers: dict[str, BaseRecommendationProvider] = {}
        self._logger = logger or LoggerFactory.get_logger(__name__)

    @property
    def provider_count(self) -> int:
        """Return the number of registered providers."""
        return len(self._providers)

    @property
    def provider_names(self) -> tuple[str, ...]:
        """Return registered provider names in priority order."""
        return tuple(p.provider_name() for p in self.get_ordered_providers())

    def register(self, provider: BaseRecommendationProvider) -> None:
        """Register a recommendation provider.

        Args:
            provider: The BaseRecommendationProvider instance to register.

        Raises:
            RecommendationValidationError: If a provider with the same name is already registered.
        """
        name = provider.provider_name()
        if name in self._providers:
            raise RecommendationValidationError(
                f"Duplicate provider registration: '{name}' is already registered."
            )
        self._providers[name] = provider
        self._logger.debug("recommendation_provider_registered", extra={"provider": name})

    def get(self, name: str) -> BaseRecommendationProvider | None:
        """Lookup a provider by name.

        Args:
            name: The provider name to look up.

        Returns:
            The provider instance, or None if not found.
        """
        return self._providers.get(name)

    def get_ordered_providers(self) -> tuple[BaseRecommendationProvider, ...]:
        """Return all registered providers sorted by priority (ascending).

        Returns:
            A tuple of providers in deterministic execution order.
        """
        return tuple(sorted(self._providers.values(), key=lambda p: p.priority()))

    def is_registered(self, name: str) -> bool:
        """Check if a provider with the given name is registered."""
        return name in self._providers

    def clear(self) -> None:
        """Remove all registered providers."""
        self._providers.clear()
