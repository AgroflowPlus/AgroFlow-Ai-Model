"""
Embedding utilities for AgroFlow AI.

Responsible for:

- Loading the embedding model
- Creating embeddings for queries
- Creating embeddings for multiple queries
"""

from sentence_transformers import SentenceTransformer

from chatbot.config import EMBEDDING_MODEL

from chatbot.logger import logger


# ============================================================
# GLOBAL MODEL CACHE
# ============================================================

_embedding_model = None


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

def load_embedding_model():

    """
    Load the embedding model once and
    reuse it throughout the application.
    """

    global _embedding_model

    if _embedding_model is not None:

        logger.info(

            "Embedding model already loaded."

        )

        return _embedding_model

    logger.info(

        f"Loading embedding model: {EMBEDDING_MODEL}"

    )

    try:

        _embedding_model = SentenceTransformer(

            EMBEDDING_MODEL

        )

        logger.info(

            "Embedding model loaded successfully."

        )

        return _embedding_model

    except Exception:

        logger.exception(

            "Failed to load embedding model."

        )

        raise


# ============================================================
# CREATE SINGLE QUERY EMBEDDING
# ============================================================

def create_query_embedding(

    embedding_model,

    question

):

    """
    Generate an embedding vector
    for a single question.
    """

    try:

        embedding = embedding_model.encode(

            question,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        logger.info(

            "Query embedding generated."

        )

        return embedding.tolist()

    except Exception:

        logger.exception(

            "Failed to generate query embedding."

        )

        raise


# ============================================================
# CREATE MULTIPLE QUERY EMBEDDINGS
# ============================================================

def create_query_embeddings(

    embedding_model,

    questions

):

    """
    Generate embeddings for multiple
    search queries.
    """

    try:

        embeddings = embedding_model.encode(

            questions,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

        logger.info(

            f"Generated embeddings for "

            f"{len(questions)} queries."

        )

        return embeddings.tolist()

    except Exception:

        logger.exception(

            "Failed to generate multiple embeddings."

        )

        raise