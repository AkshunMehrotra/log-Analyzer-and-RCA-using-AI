import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("AI_LOG_ANALYZER")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Console
console = logging.StreamHandler()
console.setFormatter(formatter)

# App Log
app_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)
app_handler.setFormatter(formatter)

# Error Log
error_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "error.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console)
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)