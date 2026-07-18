"""Canonical matching package exports.

Exports the public API of the canonical match collection layer.
"""

from .rules import CanonicalMatchingRules
from .validator import MatchValidator
from .duplicate_resolver import DuplicateMatchResolver
from .cross_validator import CrossMatchValidator
from .stats_builder import MatchStatisticsBuilder
from .validation_summary_builder import ValidationSummaryBuilder
from .builder import CanonicalMatchCollectionBuilder
from .pipeline import CanonicalMatchCollectionPipeline
from .service import CanonicalMatchCollectionService
