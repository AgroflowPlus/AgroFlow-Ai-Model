"""
Citation utilities for AgroFlow AI.

Responsible for formatting citations returned
from the knowledge base.
"""

from chatbot.logger import logger


# ============================================================
# FORMAT SINGLE CITATION
# ============================================================

def format_citation(document):

    title = document.get(

        "title",

        "Unknown Document"

    )

    source = document.get(

        "source",

        "Unknown Source"

    )

    section = document.get(

        "section",

        "General"

    )

    page_start = document.get(

        "page_start"

    )

    page_end = document.get(

        "page_end"

    )

    lines = [

        f"📄 {title}",

        f"   Source : {source}",

        f"   Section: {section}"

    ]

    if page_start is not None:

        if page_end is None:

            page_end = page_start

        if page_start == page_end:

            lines.append(

                f"   Page   : {page_start}"

            )

        else:

            lines.append(

                f"   Pages  : {page_start}-{page_end}"

            )

    return "\n".join(lines)


# ============================================================
# REMOVE DUPLICATE SOURCES
# ============================================================

def remove_duplicate_sources(

    documents

):

    unique = []

    seen = set()

    for doc in documents:

        key = (

            doc.get("title"),

            doc.get("source"),

            doc.get("section"),

            doc.get("page_start"),

            doc.get("page_end")

        )

        if key in seen:

            continue

        seen.add(key)

        unique.append(doc)

    logger.info(

        f"Unique citations: {len(unique)}"

    )

    return unique


# ============================================================
# SORT SOURCES
# ============================================================

def sort_sources(

    documents

):

    return sorted(

        documents,

        key=lambda d: (

            d.get("source", ""),

            d.get("page_start", 0)

        )

    )


# ============================================================
# BUILD SOURCES SECTION
# ============================================================

def build_citations(

    documents

):

    if not documents:

        logger.info(

            "No citations to build."

        )

        return ""

    documents = remove_duplicate_sources(

        documents

    )

    documents = sort_sources(

        documents

    )

    lines = [

        "",

        "Sources",

        "-" * 40

    ]

    for index, document in enumerate(

        documents,

        start=1

    ):

        lines.append(

            f"{index}."

        )

        lines.append(

            format_citation(document)

        )

        if index != len(documents):

            lines.append("")

    logger.info(

        f"Built {len(documents)} citation(s)."

    )

    return "\n".join(lines)