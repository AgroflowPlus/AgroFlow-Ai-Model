"""
General utility functions used across the chatbot.
"""

from datetime import datetime

from chatbot.logger import logger


# ============================================================
# DIVIDER
# ============================================================

def divider(length=70):

    return "=" * length


# ============================================================
# CURRENT TIME
# ============================================================

def current_timestamp():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )


# ============================================================
# LOGGING HELPERS
# ============================================================

def success(message):

    logger.info(message)


def info(message):

    logger.info(message)


def warning(message):

    logger.warning(message)


def error(message):

    logger.error(message)


# ============================================================
# TRUNCATE LONG TEXT
# ============================================================

def truncate(

    text,

    length=300

):

    if not text:

        return ""

    if len(text) <= length:

        return text

    return text[:length] + "..."


# ============================================================
# FORMAT SIMILARITY SCORE
# ============================================================

def format_similarity(score):

    return f"{score:.3f}"


# ============================================================
# SAFE STRING
# ============================================================

def safe_string(value):

    if value is None:

        return ""

    return str(value).strip()