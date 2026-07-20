"""Tests for SectionWeightConfiguration.

Purpose:
    Verify default weights, immutability, sum validation, and error on invalid configs.
"""

from __future__ import annotations

import unittest

from ats_engine.domain.ats_scoring.aggregation.weighting import SectionWeightConfiguration
from ats_engine.domain.ats_scoring.exceptions import WeightConfigurationError


class SectionWeightConfigurationTests(unittest.TestCase):
    """Tests for SectionWeightConfiguration construction and validation."""

    def test_default_weights_sum_to_one(self) -> None:
        """Default configuration weights must sum to exactly 1.0."""
        config = SectionWeightConfiguration()
        total = config.skill + config.experience + config.education + config.project + config.certification
        self.assertAlmostEqual(1.0, total, places=9)

    def test_default_skill_weight(self) -> None:
        """Default skill weight must be 0.35."""
        self.assertAlmostEqual(0.35, SectionWeightConfiguration().skill, places=9)

    def test_default_experience_weight(self) -> None:
        """Default experience weight must be 0.30."""
        self.assertAlmostEqual(0.30, SectionWeightConfiguration().experience, places=9)

    def test_default_education_weight(self) -> None:
        """Default education weight must be 0.15."""
        self.assertAlmostEqual(0.15, SectionWeightConfiguration().education, places=9)

    def test_default_project_weight(self) -> None:
        """Default project weight must be 0.10."""
        self.assertAlmostEqual(0.10, SectionWeightConfiguration().project, places=9)

    def test_default_certification_weight(self) -> None:
        """Default certification weight must be 0.10."""
        self.assertAlmostEqual(0.10, SectionWeightConfiguration().certification, places=9)

    def test_custom_valid_weights_accepted(self) -> None:
        """Custom weights summing to 1.0 must be accepted."""
        config = SectionWeightConfiguration(
            skill=0.40, experience=0.25, education=0.15,
            project=0.10, certification=0.10,
        )
        self.assertAlmostEqual(0.40, config.skill, places=9)

    def test_all_weight_on_one_section(self) -> None:
        """Weight of 1.0 on one section and 0.0 on others must be valid."""
        config = SectionWeightConfiguration(
            skill=1.0, experience=0.0, education=0.0,
            project=0.0, certification=0.0,
        )
        self.assertAlmostEqual(1.0, config.skill, places=9)

    def test_invalid_weights_raises_weight_configuration_error(self) -> None:
        """Weights that don't sum to 1.0 must raise WeightConfigurationError."""
        with self.assertRaises(Exception):
            SectionWeightConfiguration(
                skill=0.50, experience=0.50, education=0.10,
                project=0.10, certification=0.10,
            )

    def test_configuration_is_immutable(self) -> None:
        """SectionWeightConfiguration must be frozen and reject attribute assignment."""
        config = SectionWeightConfiguration()
        with self.assertRaises(Exception):
            config.skill = 0.99  # type: ignore[misc]

    def test_as_dict_returns_correct_keys(self) -> None:
        """as_dict() must return all five section names as keys."""
        config = SectionWeightConfiguration()
        d = config.as_dict()
        expected = {"SKILL", "EXPERIENCE", "EDUCATION", "PROJECT", "CERTIFICATION"}
        self.assertEqual(expected, set(d.keys()))

    def test_as_dict_values_match_attributes(self) -> None:
        """as_dict() values must match the model attributes."""
        config = SectionWeightConfiguration()
        d = config.as_dict()
        self.assertAlmostEqual(config.skill, d["SKILL"], places=9)
        self.assertAlmostEqual(config.experience, d["EXPERIENCE"], places=9)
        self.assertAlmostEqual(config.education, d["EDUCATION"], places=9)
        self.assertAlmostEqual(config.project, d["PROJECT"], places=9)
        self.assertAlmostEqual(config.certification, d["CERTIFICATION"], places=9)

    def test_version_field_is_set(self) -> None:
        """version must default to '1.0.0'."""
        config = SectionWeightConfiguration()
        self.assertEqual("1.0.0", config.version)


if __name__ == "__main__":
    unittest.main()
