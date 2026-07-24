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

    model = get_reranker()

    logger.info(
        "Reranking %d retrieved document(s).",
        len(documents)
    )

    # --------------------------------------------------------
    # Build Question-Document Pairs
    # --------------------------------------------------------

    pairs = [

        (

            question,

            doc.get("content", "")

        )

        for doc in documents

    ]

    # --------------------------------------------------------
    # Predict Relevance Scores
    # --------------------------------------------------------

    scores = model.predict(

        pairs

    )

    # --------------------------------------------------------
    # Attach Scores
    # --------------------------------------------------------

    for doc, score in zip(

        documents,

        scores

    ):

        doc["rerank_score"] = float(score)

    # --------------------------------------------------------
    # Sort by Score
    # --------------------------------------------------------

    documents.sort(

        key=lambda x: x["rerank_score"],

        reverse=True

    )

    logger.info(

        "Best reranker score: %.3f",

        documents[0]["rerank_score"]

    )

    logger.debug(
        "Top reranked documents:"
    )

    for index, doc in enumerate(

        documents,

        start=1

    ):

        logger.debug(

            "%d. %s | rerank_score=%.3f",

            index,

            doc.get("source", "Unknown"),

            doc["rerank_score"]

        )

    return documents