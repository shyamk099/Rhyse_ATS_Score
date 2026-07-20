"""Providers subpackage for Book 07 — Recommendation Engine.

Purpose:
    Expose BaseRecommendationProvider as the public provider interface.
    Concrete providers will be added in Milestones 7.2+.
"""

from __future__ import annotations

from ats_engine.domain.recommendation.providers.base import BaseRecommendationProvider, RecommendationAction, BaseRecommendationValidator
from ats_engine.domain.recommendation.providers.skill_provider import SkillRecommendationProvider
from ats_engine.domain.recommendation.providers.skill_rules import SkillRecommendationRules
from ats_engine.domain.recommendation.providers.skill_builder import SkillRecommendationBuilder
from ats_engine.domain.recommendation.providers.skill_validator import SkillRecommendationValidator
from ats_engine.domain.recommendation.providers.skill_statistics_builder import SkillRecommendationStatisticsBuilder

from ats_engine.domain.recommendation.providers.experience_provider import ExperienceRecommendationProvider
from ats_engine.domain.recommendation.providers.experience_rules import ExperienceRecommendationRules
from ats_engine.domain.recommendation.providers.experience_builder import ExperienceRecommendationBuilder
from ats_engine.domain.recommendation.providers.experience_validator import ExperienceRecommendationValidator
from ats_engine.domain.recommendation.providers.experience_statistics_builder import ExperienceRecommendationStatisticsBuilder

from ats_engine.domain.recommendation.providers.education_provider import EducationRecommendationProvider
from ats_engine.domain.recommendation.providers.education_rules import EducationRecommendationRules
from ats_engine.domain.recommendation.providers.education_builder import EducationRecommendationBuilder
from ats_engine.domain.recommendation.providers.education_validator import EducationRecommendationValidator
from ats_engine.domain.recommendation.providers.education_statistics_builder import EducationRecommendationStatisticsBuilder

from ats_engine.domain.recommendation.providers.project_provider import ProjectRecommendationProvider
from ats_engine.domain.recommendation.providers.project_rules import ProjectRecommendationRules
from ats_engine.domain.recommendation.providers.project_builder import ProjectRecommendationBuilder
from ats_engine.domain.recommendation.providers.project_validator import ProjectRecommendationValidator
from ats_engine.domain.recommendation.providers.project_statistics_builder import ProjectRecommendationStatisticsBuilder

from ats_engine.domain.recommendation.providers.certification_provider import CertificationRecommendationProvider
from ats_engine.domain.recommendation.providers.certification_rules import CertificationRecommendationRules
from ats_engine.domain.recommendation.providers.certification_builder import CertificationRecommendationBuilder
from ats_engine.domain.recommendation.providers.certification_validator import CertificationRecommendationValidator
from ats_engine.domain.recommendation.providers.certification_statistics_builder import CertificationRecommendationStatisticsBuilder

__all__ = [
    "BaseRecommendationProvider",
    "RecommendationAction",
    "BaseRecommendationValidator",
    "SkillRecommendationProvider",
    "SkillRecommendationRules",
    "SkillRecommendationBuilder",
    "SkillRecommendationValidator",
    "SkillRecommendationStatisticsBuilder",
    "ExperienceRecommendationProvider",
    "ExperienceRecommendationRules",
    "ExperienceRecommendationBuilder",
    "ExperienceRecommendationValidator",
    "ExperienceRecommendationStatisticsBuilder",
    "EducationRecommendationProvider",
    "EducationRecommendationRules",
    "EducationRecommendationBuilder",
    "EducationRecommendationValidator",
    "EducationRecommendationStatisticsBuilder",
    "ProjectRecommendationProvider",
    "ProjectRecommendationRules",
    "ProjectRecommendationBuilder",
    "ProjectRecommendationValidator",
    "ProjectRecommendationStatisticsBuilder",
    "CertificationRecommendationProvider",
    "CertificationRecommendationRules",
    "CertificationRecommendationBuilder",
    "CertificationRecommendationValidator",
    "CertificationRecommendationStatisticsBuilder",
]
