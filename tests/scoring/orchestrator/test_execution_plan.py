"""Tests for ExecutionPlan.

Purpose:
    Verify priority sorting, disabled scorer skipping, duplicate priority detection,
    empty registry rejection, and immutability of the plan.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.registry import ScoringRegistry
from ats_engine.domain.ats_scoring.orchestrator.execution_plan import ExecutionPlan, ExecutionPlanEntry
from ats_engine.domain.ats_scoring.exceptions import ExecutionPlanError

from tests.scoring.orchestrator.helpers import make_scorer


class ExecutionPlanBuildTests(unittest.TestCase):
    """Tests verifying ExecutionPlan.build() correctness."""

    def _make_full_registry(self) -> ScoringRegistry:
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        reg.register("EDUCATION", make_scorer("EDUCATION"), priority=300, enabled=True)
        reg.register("PROJECT", make_scorer("PROJECT"), priority=400, enabled=True)
        reg.register("CERTIFICATION", make_scorer("CERTIFICATION"), priority=500, enabled=True)
        return reg

    def test_build_returns_execution_plan(self) -> None:
        """build() must return an ExecutionPlan instance."""
        plan = ExecutionPlan.build(self._make_full_registry())
        self.assertIsInstance(plan, ExecutionPlan)

    def test_entries_are_execution_plan_entries(self) -> None:
        """Each entry in plan.entries must be an ExecutionPlanEntry NamedTuple."""
        plan = ExecutionPlan.build(self._make_full_registry())
        for entry in plan.entries:
            self.assertIsInstance(entry, ExecutionPlanEntry)

    def test_sorted_descending_by_priority(self) -> None:
        """Entries must be sorted by priority descending (highest first)."""
        plan = ExecutionPlan.build(self._make_full_registry())
        priorities = [e.priority for e in plan.entries]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_entries_contain_expected_names(self) -> None:
        """All five registered scorers must appear in the plan."""
        plan = ExecutionPlan.build(self._make_full_registry())
        names = {e.name for e in plan.entries}
        self.assertEqual({"SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"}, names)

    def test_disabled_scorers_are_skipped(self) -> None:
        """Disabled scorers must not appear in entries but must appear in skipped."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        plan = ExecutionPlan.build(reg)
        entry_names = [e.name for e in plan.entries]
        self.assertNotIn("SKILL", entry_names)
        self.assertIn("SKILL", plan.skipped)
        self.assertIn("EXPERIENCE", entry_names)

    def test_all_disabled_produces_empty_entries(self) -> None:
        """If all scorers are disabled, entries must be empty and all names in skipped."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=False)
        plan = ExecutionPlan.build(reg)
        self.assertEqual((), plan.entries)
        self.assertIn("SKILL", plan.skipped)
        self.assertIn("EXPERIENCE", plan.skipped)

    def test_registry_names_contains_all_registered(self) -> None:
        """registry_names must include both enabled and disabled scorer names."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=True)
        plan = ExecutionPlan.build(reg)
        self.assertIn("SKILL", plan.registry_names)
        self.assertIn("EXPERIENCE", plan.registry_names)

    def test_duplicate_enabled_priority_raises_execution_plan_error(self) -> None:
        """Duplicate priorities among enabled scorers must raise ExecutionPlanError."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=100, enabled=True)
        with self.assertRaises(ExecutionPlanError) as ctx:
            ExecutionPlan.build(reg)
        self.assertIn("100", str(ctx.exception))

    def test_duplicate_priority_disabled_does_not_raise(self) -> None:
        """Duplicate priorities are only an error if both scorers are enabled."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=False)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=100, enabled=True)
        # Should not raise — disabled scorer does not participate in ordering
        plan = ExecutionPlan.build(reg)
        self.assertEqual(1, len(plan.entries))

    def test_empty_registry_raises_execution_plan_error(self) -> None:
        """An empty registry must raise ExecutionPlanError."""
        reg = ScoringRegistry()
        with self.assertRaises(ExecutionPlanError):
            ExecutionPlan.build(reg)

    def test_execution_order_property(self) -> None:
        """execution_order must return scorer names in priority-descending order."""
        plan = ExecutionPlan.build(self._make_full_registry())
        order = plan.execution_order
        self.assertEqual(
            ("CERTIFICATION", "PROJECT", "EDUCATION", "EXPERIENCE", "SKILL"), order
        )

    def test_len_returns_enabled_count(self) -> None:
        """len(plan) must equal the number of enabled scorers."""
        reg = ScoringRegistry()
        reg.register("SKILL", make_scorer("SKILL"), priority=100, enabled=True)
        reg.register("EXPERIENCE", make_scorer("EXPERIENCE"), priority=200, enabled=False)
        plan = ExecutionPlan.build(reg)
        self.assertEqual(1, len(plan))

    def test_repr_is_readable(self) -> None:
        """repr(plan) must be a non-empty, informative string."""
        plan = ExecutionPlan.build(self._make_full_registry())
        r = repr(plan)
        self.assertIn("ExecutionPlan", r)
        self.assertGreater(len(r), 10)


if __name__ == "__main__":
    unittest.main()
