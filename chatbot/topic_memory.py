"""
Topic Memory

Stores the current agricultural topic
being discussed.
"""

current_topic = None


# ============================================================
# SET CURRENT TOPIC
# ============================================================

def set_topic(topic):

    global current_topic

    current_topic = topic


# ============================================================
# GET CURRENT TOPIC
# ============================================================

def get_topic():

    return current_topic


# ============================================================
# CLEAR TOPIC
# ============================================================

def clear_topic():

    global current_topic

    current_topic = None