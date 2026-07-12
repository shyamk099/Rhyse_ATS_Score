"""PDF parser implementation using PyMuPDF.

Purpose:
    Extract text per page and metadata from PDF files in a stateless, thread-safe manner.
"""

from __future__ import annotations

import os
from pathlib import Path
import fitz

from ats_engine.domain.document_processing.exceptions import CorruptedDocumentError, DocumentReadError
from ats_engine.domain.document_processing.models import RawDocument
from ats_engine.domain.document_processing.parser import DocumentParser


class PdfDocumentParser(DocumentParser):
    """Stateless PyMuPDF-based PDF text extractor."""

    def parse(self, file_path: Path) -> RawDocument:
        """Parse raw content from a PDF file.

        Args:
            file_path: Absolute path to the PDF file.
        """
        if not file_path.exists():
            raise DocumentReadError(f"File not found: {file_path}")

        try:
            file_size = os.path.getsize(file_path)
        except OSError as error:
            raise DocumentReadError(f"Failed to read file size for {file_path}: {error}") from error

        try:
            doc = fitz.open(file_path)
        except Exception as error:
            raise CorruptedDocumentError(f"Failed to open PDF document {file_path.name}: {error}") from error

        try:
            pages_list: list[str] = []
            for page in doc:
                # Extract text using PyMuPDF
                text = page.get_text() or ""
                pages_list.append(text)
            
            raw_content = "\n".join(pages_list)
            
            return RawDocument(
                filename=file_path.name,
                file_size_bytes=file_size,
                raw_content=raw_content,
                pages=tuple(pages_list),
            )
        except Exception as error:
            raise CorruptedDocumentError(f"Failed to extract text from PDF {file_path.name}: {error}") from error
        finally:
            try:
                doc.close()
            except Exception:
                pass
