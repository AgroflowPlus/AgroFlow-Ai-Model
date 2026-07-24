"""
Central logging configuration for AgroFlow AI.
"""

import logging


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logger = logging.getLogger("AgroFlowAI")

# Prevent duplicate logs
logger.propagate = False

# Default log level
logger.setLevel(logging.INFO)

# Console handler (works locally and on Render)
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(

    "[%(asctime)s] "

    "%(levelname)s | "

    "%(message)s",

    datefmt="%Y-%m-%d %H:%M:%S"

)

console_handler.setFormatter(formatter)

# Avoid duplicate handlers
if not logger.handlers:

    logger.addHandler(console_handler)