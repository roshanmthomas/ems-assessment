"""
Logger Module

Provides centralized logging configuration for the application.
"""

import logging


def setup_logger(name: str = "EMS", level: str = "INFO") -> logging.Logger:
    """
    Setup and return a configured logger.

    :param name: Logger name
    :param level: Logging level (INFO, DEBUG, ERROR)
    :return: Configured logger instance
    """
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # Avoid duplicate handlers

    log_level = getattr(logging, level.upper(), logging.INFO)

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger