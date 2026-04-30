import logging
import os
from logging.handlers import RotatingFileHandler

# Logs folder setup (Render compatibility)
if not os.path.exists("logs"):
    os.makedirs("logs")

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, # Changed from ERROR to INFO to see bot startup logs
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        # Stores logs in logs/logs.txt and rotates at 5MB
        RotatingFileHandler("logs/logs.txt", maxBytes=5000000, backupCount=5),
        logging.StreamHandler(),
    ],
)

# Set Pyrogram and other noisy libraries to WARNING only
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("tgcrypto").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Initialize logger instance
logging = logging.getLogger()
