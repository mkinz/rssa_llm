import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file="app.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_format = logging.Formatter(format_string)
    file_format = logging.Formatter(format_string)
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
