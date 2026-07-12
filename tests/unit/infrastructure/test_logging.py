"""Unit tests for logging infrastructure.

Purpose:
    Verify structured, context-aware logging, formatting, timing, and thread safety.
"""

from __future__ import annotations

import json
import logging
import threading
import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import time

from ats_engine.infrastructure.logging.context import LoggingContext
from ats_engine.infrastructure.logging.exceptions import LoggingConfigurationError
from ats_engine.infrastructure.logging.factory import LoggerFactory
from ats_engine.infrastructure.logging.formatter import StructuredFormatter
from ats_engine.infrastructure.logging.performance import log_execution_time
from ats_engine.infrastructure.logging.service import LoggingService


class LoggingInfrastructureTests(unittest.TestCase):
    """Test suite for the structured context-aware logging infrastructure."""

    def setUp(self) -> None:
        """Reset LoggingContext and LoggerFactory caches before each test."""
        LoggingContext.clear()
        LoggerFactory.clear_cache()

    def tearDown(self) -> None:
        """Reset LoggingContext and LoggerFactory caches after each test."""
        LoggingContext.clear()
        LoggerFactory.clear_cache()
        # Reset logging configuration to prevent leakage between tests
        logging.getLogger().handlers.clear()

    def test_logger_factory_creates_and_caches_loggers(self) -> None:
        """LoggerFactory gets adapted loggers and caches them for reuse."""
        logger1 = LoggerFactory.get_logger("test_logger")
        logger2 = LoggerFactory.get_logger("test_logger")
        logger3 = LoggerFactory.get_logger("other_logger")

        self.assertIs(logger1, logger2)
        self.assertIsNot(logger1, logger3)

    def test_context_storage_is_thread_safe(self) -> None:
        """LoggingContext variables are isolated between different threads."""
        LoggingContext.set("correlation_id", "main_thread")
        
        thread_context: dict[str, Any] = {}

        def thread_target() -> None:
            LoggingContext.set("correlation_id", "sub_thread")
            thread_context["correlation_id"] = LoggingContext.get("correlation_id")

        thread = threading.Thread(target=thread_target)
        thread.start()
        thread.join()

        self.assertEqual("main_thread", LoggingContext.get("correlation_id"))
        self.assertEqual("sub_thread", thread_context["correlation_id"])

    def test_context_manager_restores_previous_state(self) -> None:
        """LoggingContext manager temporarily adds variables and restores on exit."""
        LoggingContext.set("correlation_id", "outer")
        
        with LoggingContext.context(correlation_id="inner", evaluation_id="eval_1"):
            self.assertEqual("inner", LoggingContext.get("correlation_id"))
            self.assertEqual("eval_1", LoggingContext.get("evaluation_id"))

        self.assertEqual("outer", LoggingContext.get("correlation_id"))
        self.assertIsNone(LoggingContext.get("evaluation_id"))

    def test_structured_formatter_outputs_json(self) -> None:
        """StructuredFormatter output is a valid JSON string with correct metadata."""
        formatter = StructuredFormatter(include_context=True)
        logger = logging.getLogger("test_formatter")
        record = logging.LogRecord(
            name=logger.name,
            level=logging.INFO,
            pathname="test_logging.py",
            lineno=42,
            msg="Formatted message: %s",
            args=("success",),
            exc_info=None,
        )

        LoggingContext.set("correlation_id", "corr_123")
        setattr(record, "custom_field", "extra_val")
        
        json_output = formatter.format(record)
        log_data = json.loads(json_output)

        self.assertEqual("INFO", log_data["level"])
        self.assertEqual("test_formatter", log_data["logger"])
        self.assertEqual("Formatted message: success", log_data["message"])
        self.assertEqual("corr_123", log_data["context"]["correlation_id"])
        self.assertEqual("extra_val", log_data["extra"]["custom_field"])
        self.assertIn("timestamp", log_data)

    def test_log_execution_time_outputs_perf_metadata(self) -> None:
        """log_execution_time writes start and completion logs with duration."""
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter(include_context=False))
        
        logger = logging.getLogger("test_timing")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        with log_execution_time(logger, "test_operation"):
            time.sleep(0.01)

        handler.flush()
        output_lines = stream.getvalue().strip().split("\n")
        
        self.assertEqual(2, len(output_lines))
        start_log = json.loads(output_lines[0])
        complete_log = json.loads(output_lines[1])

        self.assertEqual("operation_started", start_log["message"])
        self.assertEqual("test_operation", start_log["extra"]["operation"])
        
        self.assertEqual("operation_completed", complete_log["message"])
        self.assertEqual("test_operation", complete_log["extra"]["operation"])
        self.assertGreater(complete_log["extra"]["execution_time_seconds"], 0)
        self.assertGreater(complete_log["extra"]["execution_time_ms"], 0)

    def test_logging_service_configures_stream_and_rotating_file(self) -> None:
        """LoggingService configures console stream and file rotating log handlers."""
        with TemporaryDirectory() as temp_dir:
            log_dir = Path(temp_dir) / "logs"
            LoggingService.configure(log_directory=log_dir)

            root_logger = logging.getLogger()
            self.assertEqual(2, len(root_logger.handlers))
            
            console_handler = root_logger.handlers[0]
            file_handler = root_logger.handlers[1]

            self.assertIsInstance(console_handler, logging.StreamHandler)
            self.assertIsInstance(file_handler, logging.handlers.RotatingFileHandler)
            self.assertEqual(str(log_dir / "application.log"), file_handler.baseFilename)

            # Log something to confirm it works
            logger = LoggerFactory.get_logger("test_service")
            logger.info("Service operational test")
            
            LoggingService.shutdown()

    def test_logging_service_fails_with_invalid_config(self) -> None:
        """LoggingService configuration raises LoggingConfigurationError on invalid setup."""
        with self.assertRaises(LoggingConfigurationError):
            LoggingService.configure(logging_configuration_path="nonexistent_config_file.yaml")
