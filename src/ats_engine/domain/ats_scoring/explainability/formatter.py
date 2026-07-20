"""ExplainabilityFormatter definition.

Purpose:
    Provide stateless formatting of mathematical formulas and summary strings
    for deterministic explainability outputs.
"""

from __future__ import annotations

from typing import Any
from ats_engine.domain.ats_scoring.exceptions import FormattingError


class ExplainabilityFormatter:
    """Stateless formatter responsible for formatting calculations and text summaries."""

    @staticmethod
    def format_section_formula(
        raw_score: float,
        maximum_score: float,
        weight_used: float,
        contribution: float,
    ) -> str:
        """Format the section score calculation mathematically.

        Formula representation:
            (raw_score / maximum_score) × 100 × weight_used = contribution

        Raises:
            FormattingError: If maximum_score is zero or negative.
        """
        if maximum_score <= 0:
            raise FormattingError(
                f"Cannot format formula: invalid maximum_score {maximum_score} (must be > 0)."
            )

        # Format using standard float presentation format to avoid scientific notation
        raw_str = f"{raw_score:g}"
        max_str = f"{maximum_score:g}"
        weight_str = f"{weight_used:g}"
        contrib_str = f"{contribution:.2f}".rstrip('0').rstrip('.')
        if contrib_str == "":
            contrib_str = "0"

        return f"({raw_str} / {max_str}) × 100 × {weight_str} = {contrib_str}"

    @staticmethod
    def format_section_summary(
        section_name: str,
        raw_score: float,
        maximum_score: float,
        normalized_score: float,
        weight_used: float,
        matched_count: int,
        missing_count: int,
    ) -> str:
        """Create a human-readable deterministic summary text block for a section."""
        norm_str = f"{normalized_score:.1f}".rstrip('0').rstrip('.')
        if norm_str == "":
            norm_str = "0"
        return (
            f"{section_name.title()} Score: {raw_score:g}/{maximum_score:g} "
            f"({norm_str}%). Matched: {matched_count}, Missing: {missing_count}."
        )

    @staticmethod
    def format_overall_formula(
        overall_score: float,
        contributions: dict[str, float],
    ) -> str:
        """Format the final overall score summation.

        Formula representation:
            overall_score = skill_contrib + experience_contrib + education_contrib + project_contrib + certification_contrib
        """
        keys = ["SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"]
        contrib_vals = []
        for k in keys:
            val = contributions.get(k, 0.0)
            contrib_str = f"{val:.2f}".rstrip('0').rstrip('.')
            if contrib_str == "":
                contrib_str = "0"
            contrib_vals.append(contrib_str)

        contrib_sum_str = " + ".join(contrib_vals)
        overall_str = f"{overall_score:.2f}".rstrip('0').rstrip('.')
        if overall_str == "":
            overall_str = "0"

        return f"{overall_str} = {contrib_sum_str}"

    @staticmethod
    def format_overall_summary(overall_score: float) -> str:
        """Create a human-readable deterministic summary for the overall ATS score."""
        overall_str = f"{overall_score:.2f}"
        return f"Overall ATS Score: {overall_str}/100.00."
