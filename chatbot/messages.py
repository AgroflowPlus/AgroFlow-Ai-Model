from chatbot.prompts import SYSTEM_PROMPT

from chatbot.memory import get_history


# ============================================================
# BUILD CHAT MESSAGES
# ============================================================

def build_messages(user_prompt):

    """
    Build the complete message list
    sent to the LLM.
    """

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }

    ]

    # --------------------------------------------------------
    # Conversation History
    # --------------------------------------------------------

    messages.extend(

        get_history()

    )

    # --------------------------------------------------------
    # Current User Prompt
    # --------------------------------------------------------

    messages.append(

        {

            "role": "user",

            "content": user_prompt

        }

    )

    return messages