"""
Hybrid ranking utilities.

Combines vector similarity and keyword search
into a single ranking score.
"""

from chatbot.logger import logger


# ============================================================
# COMPUTE HYBRID SCORE
# ============================================================

def compute_hybrid_scores(

    vector_docs,

    keyword_docs

):

    logger.info(
        "Computing hybrid ranking "
        "(vector=%d, keyword=%d)",
        len(vector_docs),
        len(keyword_docs)
    )

    ranked = {}

    # --------------------------------------------------------
    # Vector Results
    # --------------------------------------------------------

    for doc in vector_docs:

        doc = dict(doc)

        vector_score = doc.get("similarity", 0)

        doc["vector_score"] = vector_score
        doc["keyword_score"] = 0
        doc["hybrid_score"] = vector_score

        ranked[doc["id"]] = doc

    # --------------------------------------------------------
    # Keyword Results
    # --------------------------------------------------------

    for doc in keyword_docs:

        doc = dict(doc)

        keyword_score = doc.get("similarity", 0)

        if doc["id"] in ranked:

            ranked_doc = ranked[doc["id"]]

            ranked_doc["keyword_score"] = keyword_score

            # Bonus because BOTH searches found it
            ranked_doc["hybrid_score"] = (

                ranked_doc["vector_score"]

                +

                (keyword_score * 0.30)

                +

                0.10

            )

        else:

            doc["vector_score"] = 0
            doc["keyword_score"] = keyword_score

            doc["hybrid_score"] = (

                keyword_score * 0.50

            )

            ranked[doc["id"]] = doc

    documents = list(ranked.values())

    documents.sort(

        key=lambda x: x["hybrid_score"],

        reverse=True

    )

    if documents:

        logger.info(
            "Hybrid ranking completed. Best hybrid score: %.3f",
            documents[0]["hybrid_score"]
        )

    else:

        logger.warning(
            "Hybrid ranking produced no documents."
        )

    return documents