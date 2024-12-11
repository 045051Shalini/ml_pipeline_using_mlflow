import logging
import daiquiri

logger = None


def create_logger(log_level="info", log_dir=".ml_monitor"):
    """
    Sets up a logger with the specified log level and directory.

    Parameters:
    - log_level (str): Logging level (e.g., "info", "debug").
    - log_dir (str): Directory where log files will be stored. Use `None` for STDERR output.
    """
    global logger

    if logger is not None:
        return  # Avoid reinitializing the logger

    log_level = getattr(logging, log_level.upper())

    if log_dir is None:
        outputs = [daiquiri.output.STDERR]  # Log to STDERR if no directory is specified
    else:
        outputs = [daiquiri.output.File(directory=log_dir)]  # Log to files in the specified directory

    daiquiri.setup(level=log_level, outputs=outputs)
    logger = daiquiri.getLogger(__name__)  # Set the global logger


def debug(msg):
    """Logs a debug-level message."""
    if logger is not None:
        logger.debug(msg)


def info(msg):
    """Logs an info-level message."""
    if logger is not None:
        logger.info(msg)


def warning(msg):
    """Logs a warning-level message."""
    if logger is not None:
        logger.warning(msg)


def error(msg):
    """Logs an error-level message."""
    if logger is not None:
        logger.error(msg)
