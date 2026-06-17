"""Logger configuration for isolated-failure reporting."""

import logging
import sys

_LOGGER_NAME = "codetrace"


def get_logger() -> logging.Logger:
    """Return the shared CodeTrace logger.

    The logger writes warnings to ``stderr`` and is configured once. It is used
    to surface isolated infrastructure failures without interrupting user code.
    """
    logger = logging.getLogger(_LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
    return logger
