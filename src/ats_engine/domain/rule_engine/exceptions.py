"""Custom rule engine exceptions.

Purpose:
    Define rule-specific error classes for loading, validation, and retrieval failures.
"""

class RuleEngineError(Exception):
    """Base exception for all rule engine errors."""


class RuleLoadError(RuleEngineError):
    """Raised when reading or parsing a rule file fails."""


class RuleValidationError(RuleEngineError):
    """Raised when rule validation fails."""


class DuplicateRuleError(RuleValidationError):
    """Raised when duplicate rule identifiers are detected in a rule set."""


class RuleNotFoundError(RuleEngineError):
    """Raised when a requested rule cannot be found."""
