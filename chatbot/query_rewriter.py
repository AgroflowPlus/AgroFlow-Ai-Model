"""
Query Rewriter

Uses the LLM to rewrite user questions into
better search queries for the agricultural
knowledge base.
"""

from chatbot.llm import ask_llm
from chatbot.logger import logger


# ============================================================
# QUERY REWRITE SYSTEM PROMPT
# ============================================================

QUERY_REWRITE_SYSTEM_PROMPT = """
You are an agricultural information retrieval expert.

Your task is to rewrite user questions into
search queries that maximize retrieval from
an agricultural knowledge base.

Rules:

1. Preserve the user's original intent exactly.

2. Expand abbreviations whenever possible.

3. Include important agricultural terminology
when it improves retrieval.

4. Remove conversational or unnecessary words.

5. Keep the rewritten query concise
(typically between 5 and 15 words).

6. Do NOT answer the question.

7. Return ONLY the rewritten search query.

No explanations.
No bullet points.
No quotation marks.
"""


# ============================================================
# REWRITE QUERY
# ============================================================

def rewrite_query(

    llm,

    question

):

    logger.info("Rewriting search query.")

    messages = [

        {
            "role": "system",
            "content": QUERY_REWRITE_SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content":
                f"Rewrite this agricultural search query:\n\n"
                f"{question}"
        }

    ]

    rewritten_query = ask_llm(

        client=llm,

        messages=messages,

        temperature=0.1,

        max_tokens=100

    )

    # --------------------------------------------------------
    # Clean output
    # --------------------------------------------------------

    rewritten_query = rewritten_query.strip()

    # Remove quotation marks
    rewritten_query = rewritten_query.strip("\"'")

    # Remove labels like "Query:"
    if ":" in rewritten_query:

        rewritten_query = rewritten_query.split(
            ":",
            1
        )[-1].strip()

    # Keep only the first line
    if "\n" in rewritten_query:

        rewritten_query = rewritten_query.split(
            "\n"
        )[0].strip()

    # Remove trailing period
    rewritten_query = rewritten_query.rstrip(".")

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not rewritten_query:

        logger.warning(
            "Query rewrite returned empty response. Using original question."
        )

        rewritten_query = question

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    logger.info(
        "Query rewritten successfully."
    )

    logger.debug(
        f"Original Query: {question}"
    )

    logger.debug(
        f"Rewritten Query: {rewritten_query}"
    )

    if rewritten_query.lower() == question.lower():

        logger.debug(
            "Query remained unchanged."
        )

    return rewritten_query