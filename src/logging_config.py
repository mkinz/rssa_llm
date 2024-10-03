import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger


def setup_logging(log_file="app.log"):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler (size-based rotation)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    # Time-based rotating file handler
    timed_handler = TimedRotatingFileHandler(
        f"{log_file}.timed", when="midnight", interval=1, backupCount=7
    )
    timed_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    json_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d"
    )
    console_handler.setFormatter(json_formatter)
    file_handler.setFormatter(json_formatter)
    timed_handler.setFormatter(json_formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(timed_handler)

    return logger


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
