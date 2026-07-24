import traceback

from chatbot.database import get_supabase

from chatbot.embeddings import load_embedding_model

from chatbot.llm import get_llm

from chatbot.chat_engine import chat

from chatbot.logger import logger


# ============================================================
# START CLI
# ============================================================

def run_cli():

    print("\n" + "=" * 70)
    print("AgroFlow AI")
    print("Type 'exit' to quit.")
    print("=" * 70)

    # --------------------------------------------------------
    # Initialize Components
    # --------------------------------------------------------

    logger.info("Initializing AgroFlow AI...")

    supabase = get_supabase()

    logger.info("Supabase connected.")

    embedding_model = load_embedding_model()

    logger.info("Embedding model loaded.")

    llm = get_llm()

    logger.info("LLM initialized.")

    logger.info("AgroFlow AI is ready.")

    # --------------------------------------------------------
    # Chat Loop
    # --------------------------------------------------------

    while True:

        try:

            question = input("\nYou: ").strip()

            if not question:

                continue

            if question.lower() in {

                "exit",

                "quit",

                "bye"

            }:

                logger.info("User ended the session.")

                print("\nGoodbye!")

                break

            logger.info(

                f"User Question: {question}"

            )

            answer = chat(

                question=question,

                supabase=supabase,

                embedding_model=embedding_model,

                llm=llm

            )

            logger.info("Answer generated successfully.")

            print("\n" + "=" * 70)
            print("AgroFlow AI")
            print("=" * 70)
            print(answer)
            print("=" * 70)

        except KeyboardInterrupt:

            logger.info("Session interrupted by user.")

            print("\n\nSession terminated.")

            break

        except Exception as e:

            logger.exception(

                "Unexpected error during chat session."

            )

            print(

                "\nAn unexpected error occurred."

            )

            print(

                "Please try again."

            )