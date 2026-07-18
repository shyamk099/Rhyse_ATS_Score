"""Feature Matcher factory.

Purpose:
    Instantiate concrete FeatureMatcher instances dynamically,
    keeping factory operations stateless.
"""

from __future__ import annotations

from ats_engine.domain.matching.matcher import FeatureMatcher


class FeatureMatcherFactory:
    """Stateless factory producing dynamic instances of FeatureMatcher classes."""

    @classmethod
    def create(cls, matcher_cls: type[FeatureMatcher]) -> FeatureMatcher:
        """Instantiate the FeatureMatcher subclass.

        Args:
            matcher_cls: Type of FeatureMatcher.

        Returns:
            The instantiated FeatureMatcher object.
        """
        return matcher_cls()
