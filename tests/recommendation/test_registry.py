"""Tests for RecommendationRegistry.

Purpose:
    Verify registry registration, lookups, duplicate detection, and priority ordering.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.registry import RecommendationRegistry
from ats_engine.domain.recommendation.exceptions import RecommendationValidationError
from tests.recommendation.helpers import DummyProvider


class RecommendationRegistryTests(unittest.TestCase):
    """Test suite validating RecommendationRegistry management APIs."""

    def setUp(self) -> None:
        self.registry = RecommendationRegistry()

    def test_register_adds_provider(self) -> None:
        """Registering a provider must increase the count and make it retrievable."""
        provider = DummyProvider(name="SKILL")
        self.registry.register(provider)
        self.assertEqual(1, self.registry.provider_count)
        self.assertIs(provider, self.registry.get("SKILL"))

    def test_duplicate_registration_raises_validation_error(self) -> None:
        """Registering a duplicate provider name must raise RecommendationValidationError."""
        self.registry.register(DummyProvider(name="SKILL"))
        with self.assertRaises(RecommendationValidationError):
            self.registry.register(DummyProvider(name="SKILL"))

    def test_provider_names_returned_in_priority_order(self) -> None:
        """provider_names property must return names ordered by priority ascending."""
        p1 = DummyProvider(name="LOW", priority_val=10)
        p2 = DummyProvider(name="HIGH", priority_val=5)

        self.registry.register(p1)
        self.registry.register(p2)

        self.assertEqual(("HIGH", "LOW"), self.registry.provider_names)

    def test_clear_removes_all_providers(self) -> None:
        """clear() must empty the registry completely."""
        self.registry.register(DummyProvider(name="SKILL"))
        self.registry.clear()
        self.assertEqual(0, self.registry.provider_count)


if __name__ == "__main__":
    unittest.main()
