"""
Cross-Encoder Reranker

Uses a CrossEncoder model to rerank the retrieved
documents according to their relevance to the user's
question.
"""

from sentence_transformers import CrossEncoder

from chatbot.config import RERANKER_MODEL
from chatbot.logger import logger


# ============================================================
# SETTINGS
# ============================================================

MAX_RERANK_DOCUMENTS = 5

MIN_DOCUMENTS_TO_RERANK = 3

BATCH_SIZE = 16


# ============================================================
# GLOBAL RERANKER
# ============================================================

reranker = None


# ============================================================
# LOAD RERANKER
# ============================================================

def get_reranker():
    """
    Lazily load the CrossEncoder model.
    The model is loaded only once.
    """

    global reranker

    if reranker is None:

        logger.info(
            "Loading Cross-Encoder reranker: %s",
            RERANKER_MODEL
        )

        reranker = CrossEncoder(
            RERANKER_MODEL
        )

        logger.info(
            "Cross-Encoder reranker loaded successfully."
        )

    return reranker


# ============================================================
# RERANK DOCUMENTS
# ============================================================

def rerank_documents(
    question,
    documents
):
    """
    Rerank retrieved documents using a CrossEncoder.

    Parameters
    ----------
    question : str
        User question.

    documents : list
        Retrieved documents.

    Returns
    -------
    list
        Documents sorted by reranker relevance score.
    """

    if not documents:

        logger.info(
            "Skipping reranking because no documents were retrieved."
        )

        return []

    # --------------------------------------------------------
    # Skip reranking if very few documents
    # --------------------------------------------------------

    if len(documents) <= MIN_DOCUMENTS_TO_RERANK:

        logger.info(
            "Skipping reranking (%d document(s) only).",
            len(documents)
        )

        return documents

    # --------------------------------------------------------
    # Only rerank the top retrieved documents
    # --------------------------------------------------------

    documents_to_rerank = documents[:MAX_RERANK_DOCUMENTS]

    logger.info(
        "Reranking %d of %d retrieved document(s).",
        len(documents_to_rerank),
        len(documents)
    )

    model = get_reranker()

    # --------------------------------------------------------
    # Build Question-Document Pairs
    # --------------------------------------------------------

    pairs = [

        (

            question,

            doc.get("content", "")

        )

        for doc in documents_to_rerank

    ]

    # --------------------------------------------------------
    # Predict Relevance Scores
    # --------------------------------------------------------

    scores = model.predict(

        pairs,

        batch_size=BATCH_SIZE,

        show_progress_bar=False

    )

    # --------------------------------------------------------
    # Attach Scores
    # --------------------------------------------------------

    for doc, score in zip(

        documents_to_rerank,

        scores

    ):

        doc["rerank_score"] = float(score)

    # --------------------------------------------------------
    # Sort reranked documents
    # --------------------------------------------------------

    documents_to_rerank.sort(

        key=lambda x: x["rerank_score"],

        reverse=True

    )

    # --------------------------------------------------------
    # Keep the remaining documents
    # --------------------------------------------------------

    final_documents = documents_to_rerank + documents[MAX_RERANK_DOCUMENTS:]

    logger.info(

        "Best reranker score: %.3f",

        documents_to_rerank[0]["rerank_score"]

    )

    logger.debug(

        "Top reranked documents:"

    )

    for index, doc in enumerate(

        documents_to_rerank,

        start=1

    ):

        logger.debug(

            "%d. %s | rerank_score=%.3f",

            index,

            doc.get("source", "Unknown"),

            doc["rerank_score"]

        )

    return final_documents
