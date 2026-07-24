"""
Context compression for AgroFlow AI.

Removes duplicate retrieved documents,
sorts them by relevance, and limits
the number of chunks sent to the LLM.
"""

from chatbot.config import TOP_CONTEXT_CHUNKS

from chatbot.logger import logger


# ============================================================
# REMOVE DUPLICATE DOCUMENTS
# ============================================================

def remove_duplicate_documents(

    documents

):

    """
    Remove duplicate documents based
    on identical content.
    """

    unique = []

    seen = set()

    duplicates_removed = 0

    for doc in documents:

        content = doc.get(

            "content",

            ""

        ).strip().lower()

        if content in seen:

            duplicates_removed += 1

            continue

        seen.add(content)

        unique.append(doc)

    logger.info(

        f"Removed {duplicates_removed} duplicate document(s)."

    )

    return unique


# ============================================================
# SORT DOCUMENTS
# ============================================================

def sort_documents(

    documents

):

    """
    Sort documents by reranker score.

    Falls back to RRF score if
    rerank_score is unavailable.
    """

    return sorted(

        documents,

        key=lambda doc: (

            doc.get(

                "rerank_score",

                doc.get(

                    "rrf_score",

                    0.0

                )

            )

        ),

        reverse=True

    )


# ============================================================
# COMPRESS CONTEXT
# ============================================================

def compress_context(

    documents

):

    """
    Compress retrieved documents before
    sending them to the LLM.
    """

    if not documents:

        logger.info(

            "No documents available for context compression."

        )

        return []

    original_count = len(documents)

    documents = remove_duplicate_documents(

        documents

    )

    documents = sort_documents(

        documents

    )

    documents = documents[:TOP_CONTEXT_CHUNKS]

    logger.info(

        f"Context compressed from {original_count} "

        f"to {len(documents)} document(s)."

    )

    return documents