"""Integration tests for duplicate match handling.

Purpose:
    Verify that duplicate match IDs, feature ID pairs, or multiple category features
    are resolved correctly according to the active duplicate matching rules.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from ats_engine.domain.feature_engineering.models import CanonicalFeatureCollection
from ats_engine.domain.matching.canonical.service import CanonicalMatchCollectionService
from ats_engine.domain.matching.canonical.rules import CanonicalMatchingRules
from tests.integration.pipeline_helpers import create_matching_service


class DuplicateHandlingTests(unittest.TestCase):
    """Duplicates resolution tests."""

    def setUp(self) -> None:
        """Load duplicate-heavy feature collections."""
        res_path = Path("tests/fixtures/resume_duplicates.json")
        job_path = Path("tests/fixtures/job_duplicates.json")

        self.assertTrue(res_path.is_file())
        self.assertTrue(job_path.is_file())

        with open(res_path, "r", encoding="utf-8") as f:
            self._resume_features = CanonicalFeatureCollection.model_validate_json(f.read())
        with open(job_path, "r", encoding="utf-8") as f:
            self._job_features = CanonicalFeatureCollection.model_validate_json(f.read())

        self._match_service = create_matching_service()
        self._canonical_match_service = CanonicalMatchCollectionService()

    def test_duplicate_resolution_policies(self) -> None:
        """Verify duplicate matching results are handled correctly according to policy."""
        from ats_engine.domain.feature_engineering.models import FeatureProvenance
        from ats_engine.domain.matching.models import MatchResult, MatchMetadata, MatchLocation, MatchCollection, MatchingStatistics
        
        r1 = MatchResult(
            match_id="M1",
            matcher_type="SkillMatcher",
            resume_feature_id="R-SK-1",
            job_feature_id="J-SK-1",
            metadata=MatchMetadata(
                correlation_id="corr-test",
                matcher_type="SkillMatcher",
                execution_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
                custom_attributes={"confidence": 0.5},
            ),
            provenance=FeatureProvenance(source_entity_id="E1", source_entity_type="SKILL"),
        )
        r2 = MatchResult(
            match_id="M2",
            matcher_type="SkillMatcher",
            resume_feature_id="R-SK-1",
            job_feature_id="J-SK-1",
            metadata=MatchMetadata(
                correlation_id="corr-test",
                matcher_type="SkillMatcher",
                execution_timestamp="2026-07-13T20:00:00Z",
                rules_version="v1.0",
                custom_attributes={"confidence": 0.9},
            ),
            provenance=FeatureProvenance(source_entity_id="E1", source_entity_type="SKILL"),
        )

        skill_col = MatchCollection(
            results=(r1, r2),
            statistics=MatchingStatistics(total_resume_features=2, total_job_features=2),
        )
        empty = MatchCollection(statistics=MatchingStatistics())

        # Under default policy: KEEP_FIRST
        rules_first = CanonicalMatchingRules(duplicate_policy="KEEP_FIRST")
        res_first = self._canonical_match_service.build(
            skill_matches=skill_col,
            experience_matches=empty,
            education_matches=empty,
            project_matches=empty,
            certification_matches=empty,
            rules=rules_first,
        )
        self.assertEqual(1, len(res_first.results))
        self.assertEqual("M1", res_first.results[0].match_id)
        self.assertEqual(1, res_first.statistics.duplicate_count)

        # Under KEEP_ALL policy
        rules_all = CanonicalMatchingRules(duplicate_policy="KEEP_ALL")
        res_all = self._canonical_match_service.build(
            skill_matches=skill_col,
            experience_matches=empty,
            education_matches=empty,
            project_matches=empty,
            certification_matches=empty,
            rules=rules_all,
        )
        self.assertEqual(2, len(res_all.results))
        self.assertEqual(0, res_all.statistics.duplicate_count)

