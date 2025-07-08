"""
helpers.py
-----------
Common utility functions for the project.

Includes:
    - get_logger: Returns a configured logger instance for use across modules.
"""

import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a logger instance with a standard format and level.

    Args:
        name (Optional[str]): Name of the logger. Defaults to None (root logger).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger: logging.Logger = logging.getLogger(name)
    if not logger.handlers:
        handler: logging.StreamHandler = logging.StreamHandler()
        formatter: logging.Formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
