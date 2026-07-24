"""
History-Aware Question Rewriter

Converts follow-up questions into
standalone agricultural questions using
conversation history and the current topic.
"""

from chatbot.llm import ask_llm

from chatbot.logger import logger


# ============================================================
# SYSTEM PROMPT
# ============================================================

HISTORY_REWRITE_SYSTEM_PROMPT = """
You are an expert agricultural AI assistant.

Your task is to rewrite the user's latest question
into a complete standalone agricultural question.

You are given:

1. The current agricultural topic.
2. The recent conversation history.
3. The user's latest question.

Use BOTH the current topic and conversation history
to resolve references such as:

- it
- they
- them
- this
- that
- these
- those
- the crop
- the plant
- the disease
- the animal

Rules:

1. Preserve the user's original meaning.

2. Prefer the current topic whenever it clearly
   resolves the ambiguity.

3. Use conversation history when the topic alone
   is insufficient.

4. If the question is already standalone,
   return it unchanged.

5. Return ONLY the rewritten question.

Do not answer the question.

Do not explain your reasoning.
"""


# ============================================================
# BUILD HISTORY
# ============================================================

def build_history(

    history

):

    """
    Convert conversation history into
    plain text for the LLM.
    """

    if not history:

        return ""

    lines = []

    for message in history:

        role = message.get(

            "role",

            "User"

        ).capitalize()

        content = message.get(

            "content",

            ""

        ).strip()

        lines.append(

            f"{role}: {content}"

        )

    return "\n".join(lines)


# ============================================================
# REWRITE QUESTION
# ============================================================

def rewrite_with_history(

    llm,

    history,

    current_topic,

    question

):

    """
    Rewrite a follow-up question into
    a standalone agricultural question.
    """

    if not history and not current_topic:

        logger.info(

            "No history or topic available. Skipping history rewrite."

        )

        return question

    history_text = build_history(

        history

    )

    if not current_topic:

        current_topic = "UNKNOWN"

    messages = [

        {

            "role": "system",

            "content": HISTORY_REWRITE_SYSTEM_PROMPT

        },

        {

            "role": "user",

            "content": f"""
Current Topic:

{current_topic}

Conversation History:

{history_text}

Current Question:

{question}

Rewrite the current question into a standalone agricultural question.

Return ONLY the rewritten question.
"""

        }

    ]

    try:

        rewritten = ask_llm(

            client=llm,

            messages=messages,

            temperature=0,

            max_tokens=100

        ).strip()

    except Exception:

        logger.exception(

            "History-aware rewriting failed."

        )

        return question

    if not rewritten:

        logger.info(

            "History rewriter returned an empty response."

        )

        return question

    logger.info(

        f"History rewrite: '{question}' -> '{rewritten}'"

    )

    return rewritten