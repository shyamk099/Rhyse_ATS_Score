"""Tests for top recommendation selection.

Purpose:
    Verify top N selection preserves ordering, never re-sorts,
    and correctly handles edge cases.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.recommendation.models import Recommendation
from ats_engine.domain.recommendation.summary.summary_builder import ResumeSummaryBuilder


def _make_rec(rec_id: str, priority: int) -> Recommendation:
    return Recommendation(
        recommendation_id=rec_id,
        section="skill",
        category="SKILL_MISSING",
        title=f"Title {rec_id}",
        description=f"Description {rec_id}",
        priority=priority,
        impact=0.8,
        confidence=0.9,
    )


class TopRecommendationsTests(unittest.TestCase):
    """Test suite validating top recommendation selection logic."""

    def test_empty_list(self) -> None:
        """Empty input must return empty tuple."""
        top = ResumeSummaryBuilder.build_top_recommendations(())
        self.assertEqual(0, len(top))

    def test_fewer_than_default(self) -> None:
        """Fewer than 5 recommendations must return all."""
        recs = tuple(_make_rec(f"R{i}", 100 - i) for i in range(3))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(3, len(top))

    def test_exactly_default(self) -> None:
        """Exactly 5 recommendations must return all 5."""
        recs = tuple(_make_rec(f"R{i}", 100 - i) for i in range(5))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(5, len(top))

    def test_more_than_default(self) -> None:
        """More than 5 must return only first 5."""
        recs = tuple(_make_rec(f"R{i}", 100 - i) for i in range(10))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(5, len(top))

    def test_preserves_ordering(self) -> None:
        """Top recommendations must preserve input ordering, not re-sort."""
        recs = tuple(_make_rec(f"R{i}", 50 + i) for i in range(8))
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        for i in range(5):
            self.assertEqual(f"R{i}", top[i].recommendation_id)

    def test_custom_top_n(self) -> None:
        """Custom top_n must slice to specified count."""
        recs = tuple(_make_rec(f"R{i}", 100 - i) for i in range(10))
        top = ResumeSummaryBuilder.build_top_recommendations(recs, top_n=3)
        self.assertEqual(3, len(top))

    def test_top_n_zero(self) -> None:
        """top_n=0 must return empty tuple."""
        recs = tuple(_make_rec(f"R{i}", 100 - i) for i in range(5))
        top = ResumeSummaryBuilder.build_top_recommendations(recs, top_n=0)
        self.assertEqual(0, len(top))

    def test_single_recommendation(self) -> None:
        """Single recommendation must return that single rec."""
        recs = (_make_rec("R1", 100),)
        top = ResumeSummaryBuilder.build_top_recommendations(recs)
        self.assertEqual(1, len(top))
        self.assertEqual("R1", top[0].recommendation_id)


if __name__ == "__main__":
    unittest.main()
