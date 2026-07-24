from chatbot.config import RRF_SCORE_THRESHOLD

from chatbot.retrieval import retrieve_context

from chatbot.context_builder import build_context

from chatbot.context_compressor import compress_context

from chatbot.history_rewriter import rewrite_with_history

from chatbot.topic_extractor import extract_topic

from chatbot.topic_memory import (
    set_topic,
    get_topic
)

from chatbot.prompts import (
    build_rag_prompt,
    build_general_prompt
)

from chatbot.citations import build_citations

from chatbot.llm import ask_llm

from chatbot.memory import add_conversation

from chatbot.messages import build_messages

from chatbot.conversation_context import (
    add_user_message,
    add_assistant_message,
    get_history
)

from chatbot.logger import logger


# ============================================================
# ASK CHATBOT
# ============================================================

def chat(

    question,

    supabase,

    embedding_model,

    llm

):

    # --------------------------------------------------------
    # Get Previous Conversation History
    # --------------------------------------------------------

    history = get_history()

    logger.info(
        f"Conversation history contains {len(history)} message(s)."
    )

    # --------------------------------------------------------
    # Extract Current Topic
    # --------------------------------------------------------

    topic = extract_topic(

        llm,

        question

    )

    if topic.upper() != "UNKNOWN":

        set_topic(topic)

    logger.info(

        f"Current topic: {get_topic()}"

    )

    # --------------------------------------------------------
    # Rewrite Question Using Conversation History
    # --------------------------------------------------------

    standalone_question = rewrite_with_history(

        llm=llm,

        history=history,

        current_topic=get_topic(),

        question=question

    )

    logger.info(

        f"Standalone question: {standalone_question}"

    )

    # --------------------------------------------------------
    # Save Current User Message
    # --------------------------------------------------------

    add_user_message(question)

    # --------------------------------------------------------
    # Retrieve Documents
    # --------------------------------------------------------

    documents, best_rrf_score = retrieve_context(

        question=standalone_question,

        embedding_model=embedding_model,

        supabase=supabase,

        llm=llm

    )

    logger.info(

        f"Retrieved {len(documents)} document(s)."

    )

    # --------------------------------------------------------
    # Compress Retrieved Context
    # --------------------------------------------------------

    documents = compress_context(

        documents

    )

    logger.info(

        f"Context compressed to {len(documents)} chunk(s)."

    )

    # --------------------------------------------------------
    # Decide Whether to Use Knowledge Base
    # --------------------------------------------------------

    using_knowledge_base = (

        len(documents) > 0

        and

        best_rrf_score >= RRF_SCORE_THRESHOLD

    )

    # --------------------------------------------------------
    # Build Prompt
    # --------------------------------------------------------

    if using_knowledge_base:

        logger.info(

            f"Using Knowledge Base (Rerank Score: {best_rrf_score:.4f})"

        )

        context = build_context(

            documents

        )

        user_prompt = build_rag_prompt(

            context,

            question

        )

    else:

        logger.info(

            f"Knowledge Base skipped (Rerank Score: {best_rrf_score:.4f} < Threshold {RRF_SCORE_THRESHOLD})"

        )

        user_prompt = build_general_prompt(

            question

        )

    # --------------------------------------------------------
    # Build Conversation Messages
    # --------------------------------------------------------

    messages = build_messages(

        user_prompt

    )

    # --------------------------------------------------------
    # Ask LLM
    # --------------------------------------------------------

    logger.info(

        "Sending request to LLM..."

    )

    answer = ask_llm(

        client=llm,

        messages=messages

    )

    logger.info(

        "LLM response received."

    )

    # --------------------------------------------------------
    # Append Citations
    # --------------------------------------------------------

    if using_knowledge_base:

        citations = build_citations(

            documents

        )

        if citations:

            answer += f"\n\n{citations}"

            logger.info(

                "Citations appended."

            )

    # --------------------------------------------------------
    # Save Conversation
    # --------------------------------------------------------

    add_conversation(

        question,

        answer

    )

    # --------------------------------------------------------
    # Save Assistant Message
    # --------------------------------------------------------

    add_assistant_message(

        answer

    )

    logger.info(

        "Conversation saved."

    )

    # --------------------------------------------------------
    # Conversation Summary
    # --------------------------------------------------------

    logger.info(

        f"Conversation now contains {len(get_history())} message(s)."

    )

    # --------------------------------------------------------
    # Return Final Answer
    # --------------------------------------------------------

    return answer