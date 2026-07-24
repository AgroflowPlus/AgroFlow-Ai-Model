"""
Builds the context passed to the LLM
from retrieved knowledge base documents.
"""

from chatbot.logger import logger


# ============================================================
# FORMAT PAGE RANGE
# ============================================================

def format_pages(

    page_start,

    page_end

):

    if page_start is None:

        return "Unknown"

    if page_end is None:

        return str(page_start)

    if page_start == page_end:

        return str(page_start)

    return f"{page_start}-{page_end}"


# ============================================================
# BUILD RAG CONTEXT
# ============================================================

def build_context(

    documents

):

    """
    Convert retrieved documents into
    a structured context for the LLM.
    """

    if not documents:

        logger.info(

            "No documents available for context."

        )

        return ""

    logger.info(

        f"Building context from {len(documents)} document(s)."

    )

    context = []

    for index, doc in enumerate(

        documents,

        start=1

    ):

        title = doc.get(

            "title",

            "Unknown Document"

        )

        category = doc.get(

            "category",

            "General"

        )

        section = doc.get(

            "section",

            "General"

        )

        source = doc.get(

            "source",

            "Unknown"

        )

        similarity = doc.get(

            "similarity",

            0.0

        )

        page_start = doc.get(

            "page_start"

        )

        page_end = doc.get(

            "page_end"

        )

        content = doc.get(

            "content",

            ""

        ).strip()

        pages = format_pages(

            page_start,

            page_end

        )

        context.append(

f"""Document {index}

Title: {title}
Category: {category}
Section: {section}
Source: {source}
Pages: {pages}
Similarity: {similarity:.3f}

Content:
{content}
"""

        )

    logger.info(

        "Context successfully built."

    )

    return "\n\n".join(context)