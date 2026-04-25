# ============================================================
# Vidhi-AI | Logging Configuration
# ============================================================

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "vidhi_ai.log")


def get_logger(name: str = "vidhi_ai") -> logging.Logger:
    """Return a configured logger with file + console handlers."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)

    # File handler — rotating, max 5 MB, keep 3 backups
    fh = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    # Console handler — INFO and above
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(levelname)-8s | %(message)s"
    ))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = get_logger()
