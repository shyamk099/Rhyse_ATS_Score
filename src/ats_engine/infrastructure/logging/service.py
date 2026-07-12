"""Logging service to initialize and manage system-wide log settings.

Purpose:
    Provide programmatic configuration, level management, and lifecycle logging.
"""

from __future__ import annotations

import logging
import logging.config
import os
import yaml
from pathlib import Path
from typing import Any

from ats_engine.infrastructure.logging.exceptions import LoggingConfigurationError
from ats_engine.infrastructure.logging.factory import LoggerFactory


class LoggingService:
    """Service to configure python logging and manage logger lifecycles."""

    _configured: bool = False

    @classmethod
    def configure(
        self,
        *,
        log_directory: Path | str | None = None,
        logging_configuration_path: Path | str | None = None,
        default_level: int = logging.INFO,
    ) -> None:
        """Configure python logging subsystem.

        Args:
            log_directory: Optional path where log files will be written.
            logging_configuration_path: Optional path to a YAML configuration file.
            default_level: Default fallback log level.
        """
        # If logging config path is provided, try to load it
        config_dict: dict[str, Any] | None = None
        
        if logging_configuration_path is not None:
            config_path = Path(logging_configuration_path)
            if not config_path.is_file():
                raise LoggingConfigurationError(
                    f"Logging configuration file not found: {config_path}"
                )
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_dict = yaml.safe_load(f)
            except Exception as error:
                raise LoggingConfigurationError(
                    f"Failed to load logging config file: {config_path}"
                ) from error

        # Fallback to default configuration dictionary if not loaded
        if not config_dict:
            config_dict = self._get_default_config(log_directory, default_level)

        try:
            # Ensure directories are created for file handlers
            if log_directory is not None:
                os.makedirs(log_directory, exist_ok=True)
            elif "handlers" in config_dict:
                for handler_val in config_dict["handlers"].values():
                    if "filename" in handler_val:
                        Path(handler_val["filename"]).parent.mkdir(parents=True, exist_ok=True)

            logging.config.dictConfig(config_dict)
            self._configured = True
            
            # Startup log
            logger = LoggerFactory.get_logger("ats_engine.infrastructure.logging")
            logger.info("logging_service_configured", extra={"default_level": logging.getLevelName(default_level)})
        except Exception as error:
            raise LoggingConfigurationError(f"Failed to configure logging dictionary: {error}") from error

    @classmethod
    def shutdown(cls) -> None:
        """Perform orderly logging shutdown, flushing all handlers."""
        if cls._configured:
            logger = LoggerFactory.get_logger("ats_engine.infrastructure.logging")
            logger.info("logging_service_shutting_down")
        logging.shutdown()
        cls._configured = False

    @classmethod
    def _get_default_config(cls, log_directory: Path | str | None, default_level: int) -> dict[str, Any]:
        """Generate a default configuration dict for console and optional file logging."""
        handlers: dict[str, Any] = {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "structured",
                "level": default_level,
            }
        }
        
        if log_directory is not None:
            log_dir_path = Path(log_directory)
            handlers["file"] = {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "structured",
                "filename": str(log_dir_path / "application.log"),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "encoding": "utf-8",
                "level": default_level,
            }

        root_handlers = ["console", "file"] if "file" in handlers else ["console"]

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "structured": {
                    "()": "ats_engine.infrastructure.logging.formatter.StructuredFormatter",
                    "include_context": True,
                }
            },
            "handlers": handlers,
            "root": {
                "handlers": root_handlers,
                "level": default_level,
            },
        }
