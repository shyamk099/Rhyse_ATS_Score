"""Integration tests for the End-to-End Validation Pipeline Runner.

Purpose:
    Verify that the runner script successfully processes PDF and DOCX,
    handles empty files, unsupported files, and corrupted files gracefully,
    and returns correct exit codes.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class PipelineRunnerIntegrationTests(unittest.TestCase):
    """Test suite validating run_pipeline.py CLI commands and responses."""

    def setUp(self) -> None:
        """Define target paths for verification."""
        self._runner_script = Path("scripts/run_pipeline.py")
        self._samples_dir = Path("samples")
        self._output_dir = Path("output")

        # Verify sample files exist
        self.assertTrue(self._runner_script.is_file(), "run_pipeline.py script not found")
        self.assertTrue(self._samples_dir.is_dir(), "samples directory not found")

    def test_pipeline_success_with_pdf(self) -> None:
        """Runner runs successfully on a valid PDF resume with exit code 0 and output creation."""
        pdf_path = self._samples_dir / "resume.pdf"
        self.assertTrue(pdf_path.is_file())

        result = subprocess.run(
            [sys.executable, str(self._runner_script), str(pdf_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, f"Pipeline failed: {result.stderr}")
        self.assertIn("Pipeline executed successfully", result.stdout)

        # Check outputs exist
        self.assertTrue((self._output_dir / "canonical_document.json").is_file())
        self.assertTrue((self._output_dir / "canonical_entity_collection.json").is_file())
        self.assertTrue((self._output_dir / "pipeline_summary.md").is_file())

    def test_pipeline_success_with_docx(self) -> None:
        """Runner runs successfully on a valid DOCX resume with exit code 0."""
        docx_path = self._samples_dir / "resume.docx"
        self.assertTrue(docx_path.is_file())

        result = subprocess.run(
            [sys.executable, str(self._runner_script), str(docx_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, f"Pipeline failed: {result.stderr}")
        self.assertIn("Pipeline executed successfully", result.stdout)

    def test_pipeline_failure_with_empty_resume(self) -> None:
        """Runner fails or stops on an empty resume due to integrity validation."""
        pdf_path = self._samples_dir / "empty.pdf"
        self.assertTrue(pdf_path.is_file())

        result = subprocess.run(
            [sys.executable, str(self._runner_script), str(pdf_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        # Should fail due to IntegrityValidationError (empty layout)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("PIPELINE RUNNER EXCEPTION ENCOUNTERED", result.stdout)

    def test_pipeline_failure_with_corrupted_pdf(self) -> None:
        """Runner fails on a corrupted PDF file."""
        pdf_path = self._samples_dir / "corrupted.pdf"
        self.assertTrue(pdf_path.is_file())

        result = subprocess.run(
            [sys.executable, str(self._runner_script), str(pdf_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("PIPELINE RUNNER EXCEPTION ENCOUNTERED", result.stdout)

    def test_pipeline_failure_with_unsupported_format(self) -> None:
        """Runner fails on an unsupported file type."""
        txt_path = self._samples_dir / "unsupported.txt"
        self.assertTrue(txt_path.is_file())

        result = subprocess.run(
            [sys.executable, str(self._runner_script), str(txt_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("PIPELINE RUNNER EXCEPTION ENCOUNTERED", result.stdout)
