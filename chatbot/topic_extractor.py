"""
Topic Extractor

Extracts the primary agricultural topic
from a user's question.
"""

from chatbot.llm import ask_llm
from chatbot.logger import logger


# ============================================================
# SYSTEM PROMPT
# ============================================================

TOPIC_EXTRACTION_SYSTEM_PROMPT = """
You are an agricultural topic extractor.

Your task is to identify the SINGLE most important
agricultural topic from the user's latest message.

The topic may be:

• Crop
• Livestock
• Disease
• Pest
• Fertilizer
• Soil
• Irrigation
• Farm equipment
• Agricultural practice

Rules:

1. Return only ONE topic.

2. Keep it short.

3. Do not explain.

4. Do not answer the question.

5. If no agricultural topic exists,
return:

UNKNOWN
"""


# ============================================================
# EXTRACT TOPIC
# ============================================================

def extract_topic(

    llm,

    question

):

    logger.info("Extracting conversation topic.")

    messages = [

        {

            "role": "system",

            "content": TOPIC_EXTRACTION_SYSTEM_PROMPT

        },

        {

            "role": "user",

            "content": question

        }

    ]

    topic = ask_llm(

        client=llm,

        messages=messages,

        temperature=0,

        max_tokens=20

    )

    topic = topic.strip()

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not topic:

        logger.warning(
            "Topic extractor returned an empty response."
        )

        topic = "UNKNOWN"

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    logger.info(
        "Topic extracted successfully."
    )

    logger.debug(
        "Question: %s",
        question
    )

    logger.debug(
        "Extracted Topic: %s",
        topic
    )

    return topic