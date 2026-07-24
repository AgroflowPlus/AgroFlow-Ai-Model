"""
Prompt templates used throughout AgroFlow AI.
"""

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are AgroFlow AI, an expert agricultural assistant.

You specialize in:

• Crop production
• Soil science
• Fertilizer management
• Irrigation
• Crop diseases
• Pest management
• Livestock
• Climate-smart agriculture
• Sustainable farming
• Agricultural technology
• Agricultural economics
• Food production

==================================================
GROUNDING RULES
==================================================

Your highest priority is to answer from the AgroFlow Knowledge Base whenever
relevant information has been retrieved.

Never pretend information came from the Knowledge Base if it did not.

Never invent facts.

Never fabricate citations.

Never fabricate page numbers.

If the retrieved documents fully answer the user's question:

• Answer ONLY from the retrieved documents.

If the retrieved documents partially answer the question:

• Start with the retrieved information.

• Clearly label any additional explanation as:

General Agricultural Knowledge

If no retrieved documents are supplied:

• Answer using your agricultural expertise.

• Do NOT mention the Knowledge Base.

==================================================
RESPONSE FORMAT
==================================================

Whenever retrieved documents exist, structure your response like this:

Knowledge Base

<answer>

General Agricultural Knowledge
(Only if additional explanation is needed.)

<additional explanation>

Sources

<citations>

==================================================
QUALITY RULES
==================================================

• Be factual.

• Be concise.

• Be practical.

• Prefer bullet points whenever appropriate.

• Use numbered steps for recommendations.

• If the retrieved documents do not contain enough information,
say so clearly instead of guessing.

• Never hallucinate information.

==================================================
SCOPE
==================================================

Answer agriculture-related questions only.

If the user asks something unrelated to agriculture,
politely explain that AgroFlow AI specializes in agriculture and farming.
"""


# ============================================================
# BUILD RAG PROMPT
# ============================================================

def build_rag_prompt(

    context,

    question

):

    return f"""
You have been provided with retrieved documents from the AgroFlow Knowledge Base.

Answer the user's question using these documents as your PRIMARY source.

Important Rules

1. Every factual statement should come from the retrieved documents whenever possible.

2. Never invent facts.

3. If the documents do not contain enough information,
clearly state that the Knowledge Base does not provide the missing information.

4. If you add your own agricultural expertise,
place it under:

General Agricultural Knowledge

5. Never mix retrieved facts with outside knowledge
without clearly labeling them.

==================================================
Retrieved Documents
==================================================

{context}

==================================================
User Question
==================================================

{question}

==================================================
Required Response Format
==================================================

Knowledge Base

...

General Agricultural Knowledge
(Only if needed.)

...

Sources

...
"""


# ============================================================
# BUILD GENERAL PROMPT
# ============================================================

def build_general_prompt(question):

    """
    Used when no relevant document
    was retrieved.
    """

    return f"""
Answer the following agriculture-related question using your agricultural expertise.

Question:

{question}

Requirements:

• Be accurate.

• Be practical.

• Use bullet points whenever appropriate.

• If the answer involves recommendations,
explain them step-by-step.

• If you are uncertain,
say so instead of guessing.
"""


# ============================================================
# BUILD CITATION
# ============================================================

def build_citation(document):

    """
    Builds a citation string from
    document metadata.
    """

    source = document.get("source", "Unknown")

    start = document.get("page_start")

    end = document.get("page_end")

    if start and end:

        if start == end:

            return f"{source} (Page {start})"

        return f"{source} (Pages {start}-{end})"

    return source


# ============================================================
# BUILD DOCUMENT HEADER
# ============================================================

def build_document_header(document):

    title = document.get("title", "Unknown")

    category = document.get("category", "General")

    section = document.get("section", "General")

    source = document.get("source", "Unknown")

    return f"""
Title: {title}
Category: {category}
Section: {section}
Source: {source}
"""


# ============================================================
# BUILD QUERY REWRITE PROMPT
# ============================================================

def build_query_rewrite_prompt(question):

    """
    Reserved for future query rewriting.
    """

    return f"""
Rewrite the following agricultural question into
three improved search queries while preserving
its original meaning.

Question:

{question}
"""


# ============================================================
# BUILD SUMMARIZATION PROMPT
# ============================================================

def build_summary_prompt(text):

    """
    Reserved for future document summarization.
    """

    return f"""
Summarize the following agricultural document.

Focus on:

• Main topic

• Key findings

• Recommendations

Document:

{text}
"""