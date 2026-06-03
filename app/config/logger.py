import logging
import os
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "logs"))
LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)


def ensure_log_directory() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    ensure_log_directory()

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    file_handler = TimedRotatingFileHandler(
        LOG_PATH,
        when="midnight",
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger("app")
    if not logger.handlers:
        logger.setLevel(level)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.propagate = False

    logger.info("Logging initialized")
    logger.info(f"Log file path: {LOG_PATH}")
    return logger


def get_logger(name: str = "app") -> logging.Logger:
    return logging.getLogger(name)
