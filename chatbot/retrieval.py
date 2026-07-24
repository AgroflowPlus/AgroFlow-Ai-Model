from chatbot.config import TOP_K

from chatbot.query_rewriter import rewrite_query
from chatbot.multi_query import generate_multi_queries

from chatbot.embeddings import create_query_embedding

from chatbot.database import (
    retrieve_documents,
    keyword_search
)

from chatbot.rrf import reciprocal_rank_fusion

from chatbot.reranker import rerank_documents

from chatbot.context_compressor import compress_context

from chatbot.logger import logger


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_context(

    question,

    embedding_model,

    supabase,

    llm,

    match_count=TOP_K

):

    logger.info("Starting retrieval pipeline.")

    # --------------------------------------------------------
    # Rewrite Query
    # --------------------------------------------------------

    try:

        search_query = rewrite_query(

            llm,

            question

        )

        if not search_query.strip():

            search_query = question

    except Exception as e:

        logger.exception(
            "Query rewriting failed. Using original question."
        )

        search_query = question

    # --------------------------------------------------------
    # Generate Multiple Queries
    # --------------------------------------------------------

    try:

        search_queries = generate_multi_queries(

            llm,

            search_query

        )

        if not search_queries:

            search_queries = [search_query]

    except Exception:

        logger.exception(
            "Multi-query generation failed. Using rewritten query only."
        )

        search_queries = [search_query]

    logger.info(
        "Generated %d search quer%s.",
        len(search_queries),
        "y" if len(search_queries) == 1 else "ies"
    )

    # --------------------------------------------------------
    # Vector Search
    # --------------------------------------------------------

    vector_rank_lists = []

    for query in search_queries:

        logger.info(
            "Vector search: %s",
            query
        )

        embedding = create_query_embedding(

            embedding_model,

            query

        )

        docs, _ = retrieve_documents(

            supabase=supabase,

            embedding=embedding,

            match_count=match_count

        )

        if docs:

            vector_rank_lists.append(docs)

            logger.info(
                "Retrieved %d vector document(s).",
                len(docs)
            )

        else:

            logger.info(
                "No vector documents retrieved."
            )

    # --------------------------------------------------------
    # Keyword Search
    # --------------------------------------------------------

    keyword_docs = keyword_search(

        supabase=supabase,

        question=search_query,

        match_count=match_count

    )

    logger.info(
        "Keyword search returned %d document(s).",
        len(keyword_docs)
    )

    # --------------------------------------------------------
    # Reciprocal Rank Fusion
    # --------------------------------------------------------

    rank_lists = vector_rank_lists.copy()

    if keyword_docs:

        rank_lists.append(

            keyword_docs

        )

    documents = reciprocal_rank_fusion(

        rank_lists

    )

    logger.info(
        "RRF produced %d document(s).",
        len(documents)
    )

    # --------------------------------------------------------
    # Cross-Encoder Reranking
    # --------------------------------------------------------

    documents = rerank_documents(

        question,

        documents

    )

    logger.info(
        "Reranker returned %d document(s).",
        len(documents)
    )

    # --------------------------------------------------------
    # Context Compression
    # --------------------------------------------------------

    documents = compress_context(

        documents

    )

    logger.info(
        "Context compressed to %d document(s).",
        len(documents)
    )

    # --------------------------------------------------------
    # Final Score
    # --------------------------------------------------------

    if documents:

        best_score = documents[0].get(

            "rerank_score",

            0

        )

    else:

        best_score = 0

    logger.info(
        "Best reranker score: %.3f",
        best_score
    )

    logger.debug(
        "Final retrieved documents:"
    )

    for index, doc in enumerate(

        documents,

        start=1

    ):

        logger.debug(

            "%d. %s | RRF=%.6f | Rerank=%.3f",

            index,

            doc.get(

                "source",

                "Unknown"

            ),

            doc.get(

                "rrf_score",

                0

            ),

            doc.get(

                "rerank_score",

                0

            )

        )

    logger.info(
        "Retrieval pipeline completed successfully."
    )

    return documents, best_score