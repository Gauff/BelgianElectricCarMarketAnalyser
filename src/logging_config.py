import logging
import os

from src.config import PROJECT_ROOT


# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logging(name):
    """
    Set up logging for a given module.

    Args:
        name (str): The name of the module requesting logging (typically __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only add handlers if the logger doesn't already have them
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(
            os.path.join(LOGS_DIR, f'{name.split(".")[-1]}.log')
        )

        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
