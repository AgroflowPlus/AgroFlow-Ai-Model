"""
LLM utilities for AgroFlow AI.

Responsible for:

- Creating the Groq client
- Sending prompts to the LLM
- Returning generated responses
"""

import os

from dotenv import load_dotenv

from groq import Groq

from chatbot.logger import logger

from chatbot.config import (

    LLM_MODEL,

    TEMPERATURE,

    MAX_TOKENS

)

load_dotenv()


# ============================================================
# GLOBAL CLIENT CACHE
# ============================================================

_llm_client = None


# ============================================================
# CREATE GROQ CLIENT
# ============================================================

def get_llm():

    """
    Create the Groq client once and
    reuse it throughout the application.
    """

    global _llm_client

    if _llm_client is not None:

        logger.info(

            "Groq client already initialized."

        )

        return _llm_client

    api_key = os.getenv(

        "GROQ_API_KEY"

    )

    if not api_key:

        raise ValueError(

            "GROQ_API_KEY is missing."

        )

    try:

        _llm_client = Groq(

            api_key=api_key

        )

        logger.info(

            "Groq client initialized."

        )

        return _llm_client

    except Exception:

        logger.exception(

            "Failed to initialize Groq client."

        )

        raise


# ============================================================
# GENERATE RESPONSE
# ============================================================

def ask_llm(

    client,

    messages,

    temperature=TEMPERATURE,

    max_tokens=MAX_TOKENS

):

    """
    Send a chat completion request
    to Groq.
    """

    try:

        response = client.chat.completions.create(

            model=LLM_MODEL,

            messages=messages,

            temperature=temperature,

            max_tokens=max_tokens

        )

        answer = response.choices[0].message.content

        logger.info(

            f"Groq response generated using model '{LLM_MODEL}'."

        )

        return answer

    except Exception:

        logger.exception(

            "Groq request failed."

        )

        raise