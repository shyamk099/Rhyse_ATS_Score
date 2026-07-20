"""Determinism tests for the Scoring Engine.

Purpose:
    Verify that 100 repeated executions over the same inputs return structurally identical results.
"""

from __future__ import annotations

import hashlib
import json
import unittest

from ats_engine.domain.matching.models import CanonicalMatchCollection, MatchStatistics, ValidationSummary
from ats_engine.domain.ats_scoring.service import ScoringService
from ats_engine.domain.ats_scoring.rules import ScoringRules
from ats_engine.domain.ats_scoring.interfaces import AbstractScorer
from ats_engine.domain.ats_scoring.models.scoring_context import ScoringContext
from ats_engine.domain.ats_scoring.models.section_score import SectionScore


class DeterministicDummyScorer(AbstractScorer):
    def validate(self, context: ScoringContext) -> None:
        pass
    def score(self, context: ScoringContext) -> SectionScore:
        return SectionScore(section_name="SKILL", raw_score=95.0)
    def build(self, context: ScoringContext) -> SectionScore:
        return self.score(context)
    def statistics(self) -> dict:
        return {}
    def metadata(self) -> dict:
        return {}


class ScoringDeterminismTests(unittest.TestCase):
    """Test suite validating Scoring determinism properties."""

    def test_scoring_determinism(self) -> None:
        service = ScoringService()
        service.registry.register("SKILL", DeterministicDummyScorer)

        collection = CanonicalMatchCollection(
            results=(),
            statistics=MatchStatistics(),
            validation_summary=ValidationSummary(),
        )
        rules = ScoringRules()

        hashes: set[str] = set()

        for _ in range(100):
            res = service.score(collection, rules)
            data = res.model_dump_json()

            # Ignore dynamic timestamps and timings to check structure
            data_dict = json.loads(data)
            data_dict["metadata"]["generated_at"] = "2026-07-19T00:00:00Z"
            data_dict["metadata"]["processing_time_ms"] = 0.0
            data_dict["statistics"]["processing_time_ms"] = 0.0

            normalized_json = json.dumps(data_dict, sort_keys=True)
            sha = hashlib.sha256(normalized_json.encode("utf-8")).hexdigest()
            hashes.add(sha)

        self.assertEqual(1, len(hashes), f"Non-deterministic execution detected! Generated {len(hashes)} different hashes: {hashes}")
