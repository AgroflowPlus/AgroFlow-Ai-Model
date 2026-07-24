"""
Conversation Context

Keeps track of the current conversation topic
to resolve follow-up questions.
"""

from collections import deque


# ============================================================
# CONVERSATION HISTORY
# ============================================================

MAX_HISTORY = 10

conversation_history = deque(maxlen=MAX_HISTORY)


# ============================================================
# ADD USER MESSAGE
# ============================================================

def add_user_message(message):

    conversation_history.append({

        "role": "user",

        "content": message

    })


# ============================================================
# ADD ASSISTANT MESSAGE
# ============================================================

def add_assistant_message(message):

    conversation_history.append({

        "role": "assistant",

        "content": message

    })


# ============================================================
# GET HISTORY
# ============================================================

def get_history():

    return list(conversation_history)


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    conversation_history.clear()