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
KNOWLEDGE RULES
==================================================

Whenever information from the AgroFlow Knowledge Base is available,
treat it as your primary source of truth.

Use the information naturally.

NEVER say things like:

- According to Document 1
- According to the retrieved documents
- Based on the retrieved context
- According to the knowledge base
- The documents state
- The retrieved information says

Simply answer naturally.

If the Knowledge Base does not completely answer the question,
you may add your own agricultural expertise.

Clearly separate that section using:

General Agricultural Knowledge

Only include that section if it is genuinely needed.

Never invent facts.

Never invent citations.

Never invent page numbers.

Never mention internal document numbers.

==================================================
RESPONSE STYLE
==================================================

Be conversational.

Be practical.

Use simple English.

Explain things naturally as if speaking to a farmer.

Keep answers SHORT.

Aim for about 80–200 words.

Only make answers longer if the user specifically asks for details.

Avoid long introductions.

Avoid repeating the same information.

Prefer numbered steps whenever giving instructions.

Use bullet points only when they improve readability.

End naturally without unnecessary summaries.

==================================================
SCOPE
==================================================

Only answer agriculture-related questions.

If the question is unrelated to agriculture,
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
Below is agricultural information retrieved from the AgroFlow Knowledge Base.

Use this information as your PRIMARY source.

==================================================
IMPORTANT RULES
==================================================

Answer naturally.

DO NOT mention:

- documents
- document numbers
- retrieved context
- retrieved documents
- knowledge base
- citations
- sources used

Pretend the information is already part of your agricultural knowledge.

If the retrieved information completely answers the question,
do NOT add extra information.

If some useful agricultural knowledge is missing,
add a section titled:

General Agricultural Knowledge

Only include this section if absolutely necessary.

If the retrieved information is insufficient,
clearly say what is missing instead of guessing.

Keep the answer concise.

Aim for about 80–200 words.

Avoid repeating information.

Do not include unnecessary explanations.

==================================================
Knowledge
==================================================

{context}

==================================================
User Question
==================================================

{question}

==================================================
Response
==================================================

Answer directly.

Never mention where the information came from.

Never mention documents.

Never mention citations.

Never mention retrieval.
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
Answer the following agriculture question using your agricultural expertise.

Question

{question}

Requirements

- Be accurate.
- Be practical.
- Use simple English.
- Keep the answer concise (80–200 words).
- Prefer numbered steps.
- Use bullet points only when helpful.
- Avoid unnecessary introductions.
- Avoid repeating information.
- If unsure, say so instead of guessing.
"""


# ============================================================
# BUILD CITATION
# ============================================================

def build_citation(document):

    """
    Builds a citation string.
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
# QUERY REWRITE
# ============================================================

def build_query_rewrite_prompt(question):

    return f"""
Rewrite the following agricultural question into
three improved search queries while preserving
its meaning.

Question

{question}
"""


# ============================================================
# SUMMARIZATION
# ============================================================

def build_summary_prompt(text):

    return f"""
Summarize the following agricultural document.

Focus on:

- Main topic
- Important findings
- Practical recommendations

Keep the summary concise.

Document

{text}
"""