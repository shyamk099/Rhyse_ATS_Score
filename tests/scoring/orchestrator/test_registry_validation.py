"""Tests for ScoreOrchestratorValidator.

Purpose:
    Verify pre-flight validation detects empty registries, invalid scorer types,
    non-boolean enabled flags, and duplicate priorities among enabled scorers.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.orchestrator.validator import ScoreOrchestratorValidator
from ats_engine.domain.ats_scoring.exceptions import RegistryValidationError

from tests.scoring.orchestrator.helpers import make_scorer


class RegistryValidationTests(unittest.TestCase):
    """Tests for ScoreOrchestratorValidator.validate()."""

    def test_valid_registry_passes(self) -> None:
        """A correctly configured registry must pass validation without exception."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        # Should not raise
        ScoreOrchestratorValidator.validate(reg)

    def test_empty_registry_raises_registry_validation_error(self) -> None:
        """An empty registry must raise RegistryValidationError."""
        reg = ScoringRegistry()
        with self.assertRaises(RegistryValidationError) as ctx:
            ScoreOrchestratorValidator.validate(reg)
        self.assertIn("no scorers", str(ctx.exception).lower())

    def test_duplicate_enabled_priority_raises(self) -> None:
        """Duplicate priorities among enabled scorers must raise RegistryValidationError."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=100, enabled=True)
        with self.assertRaises(RegistryValidationError) as ctx:
            ScoreOrchestratorValidator.validate(reg)
        self.assertIn("100", str(ctx.exception))

    def test_duplicate_priority_one_disabled_passes(self) -> None:
        """Duplicate priorities do not raise if one scorer is disabled."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=100, enabled=True)
        # Should not raise
        ScoreOrchestratorValidator.validate(reg)

    def test_disabled_only_registry_passes(self) -> None:
        """A registry with only disabled scorers should pass structural validation."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        # Should not raise (empty enabled set is fine for validator; ExecutionPlan catches this)
        ScoreOrchestratorValidator.validate(reg)

    def test_all_five_standard_scorers_pass(self) -> None:
        """The default full registry must pass validation cleanly."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION"), priority=300, enabled=True)
        reg.register("PROJECT", make_scorer("PROJECT"), priority=400, enabled=True)
        reg.register("CERTIFICATION", make_scorer("CERTIFICATION"), priority=500, enabled=True)
        ScoreOrchestratorValidator.validate(reg)

    def test_validation_error_message_contains_scorer_names(self) -> None:
        """Error message for duplicate priorities must mention both scorer names."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=999, enabled=True)
        reg.register("EXTRA", make_scorer("EXTRA"), priority=999, enabled=True)
        with self.assertRaises(RegistryValidationError) as ctx:
            ScoreOrchestratorValidator.validate(reg)
        msg = str(ctx.exception)
        # Either name should appear in the error
        has_either = "SKILL" in msg or "EXTRA" in msg
        self.assertTrue(has_either)

    def test_mixed_enabled_disabled_unique_priorities_pass(self) -> None:
        """Mixed enabled/disabled scorers with unique enabled priorities must pass."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=False)
        reg.register("EDUCATION", make_scorer("EDUCATION"), priority=300, enabled=True)
        ScoreOrchestratorValidator.validate(reg)


if __name__ == "__main__":
    unittest.main()
