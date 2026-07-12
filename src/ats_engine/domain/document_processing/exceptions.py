"""Dedicated parser exception hierarchy for Document Processing.

Purpose:
    Define domain-specific error classes for file reading, format validation,
    corruption, and text normalization failures.
"""

class DocumentProcessingError(Exception):
    """Base exception for all document processing errors."""


class UnsupportedFormatError(DocumentProcessingError):
    """Raised when the document format is not supported (e.g. unknown magic bytes)."""


class CorruptedDocumentError(DocumentProcessingError):
    """Raised when a document is corrupted and cannot be read by its parser."""


class DocumentReadError(DocumentProcessingError):
    """Raised when the document file cannot be read from disk (e.g. permission or locking issues)."""


class NormalizationError(DocumentProcessingError):
    """Raised when the text normalization pipeline encounters an unrecoverable failure."""


class SegmentValidationError(DocumentProcessingError):
    """Raised when structural layout segment validation checks fail."""


class CanonicalDocumentValidationError(DocumentProcessingError):
    """Base exception for all canonical document validation errors."""


class IntegrityValidationError(CanonicalDocumentValidationError):
    """Raised when structural integrity audits fail."""


class ConsistencyValidationError(CanonicalDocumentValidationError):
    """Raised when cross-model consistency audits fail."""


class StatisticsValidationError(CanonicalDocumentValidationError):
    """Raised when document statistics compilation checks fail."""


class AssemblyValidationError(CanonicalDocumentValidationError):
    """Raised when packaging models into a CanonicalDocument fails."""
