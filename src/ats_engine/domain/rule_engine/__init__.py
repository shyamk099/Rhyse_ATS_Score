"""Rule engine infrastructure foundation package.

Purpose:
    Provide loading, validation, caching, and runtime exposure of rule envelopes.
"""

from ats_engine.domain.rule_engine.cache import RuleCache
from ats_engine.domain.rule_engine.exceptions import (
    DuplicateRuleError,
    RuleEngineError,
    RuleLoadError,
    RuleNotFoundError,
    RuleValidationError,
)
from ats_engine.domain.rule_engine.loader import RuleLoader
from ats_engine.domain.rule_engine.models import RuleEnvelope, RuleMetadata
from ats_engine.domain.rule_engine.provider import RuntimeRuleProvider
from ats_engine.domain.rule_engine.registry import RuleRegistry
from ats_engine.domain.rule_engine.service import RuleEngineService
from ats_engine.domain.rule_engine.validator import RuleValidator

__all__ = [
    "RuleCache",
    "DuplicateRuleError",
    "RuleEngineError",
    "RuleLoadError",
    "RuleNotFoundError",
    "RuleValidationError",
    "RuleLoader",
    "RuleEnvelope",
    "RuleMetadata",
    "RuntimeRuleProvider",
    "RuleRegistry",
    "RuleEngineService",
    "RuleValidator",
]
