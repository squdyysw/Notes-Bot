"""
Logger configuration module.

This module configures a project-wide logger. It ensures that
the log directory exists, sets up the base logging configuration,
and exposes a logger object for import in other modules.
"""

import logging
import os
from config import LOG_PATH, LOG_LEVEL


def setup_logger() -> logging.Logger:
    """
    Configure and return a logger instance.

    This function:
      - Creates the log directory if it doesn't exist.
      - Configures logging settings such as level, file path, and format.
      - Returns a ready-to-use logger object.

    Returns:
        logging.Logger: Configured logger instance.
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    logging.basicConfig(
        filename=LOG_PATH,
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger_instance = logging.getLogger(__name__)
    return logger_instance


# Global logger instance to be imported in other files
logger = setup_logger()
