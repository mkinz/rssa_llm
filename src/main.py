import time
import os
from logging_config import setup_logging
from valid_html import validate_llm_html
from rag_elements.vector_store import VectorStore
from rag_elements.embedding import EmbeddingModel
from llm_interface import (
    OpenAIProvider,
    CohereAIProvider,
    AnthropicAIProvider,
)
from roadmap_output_ingestor import preprocess_roadmap_output
from output_handler import get_output_handler
from input_handler import get_input_handler

logger = setup_logging()


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info(f"{method.__name__} took {te - ts:.2f} seconds")
        return result

    return timed


@timeit
def load_vector_store(file_path):
    return VectorStore.load(file_path)


@timeit
def embed_user_data(embedding_model: EmbeddingModel, user_data):
    return embedding_model.embed(user_data)


@timeit
def search_relevant_rules(vector_store: VectorStore, user_vector):
    return vector_store.search(user_vector)


@timeit
def analyze_with_llm(llm, query, context):
    return llm.analyze(query, context)


def get_openai_provider():
    return OpenAIProvider()


def get_anthropic_provider():
    return AnthropicAIProvider()


def get_cohere_provider():
    return CohereAIProvider()


def main():
    logger.info("Starting main function")

    llm_strategy = {
        "openai": get_openai_provider,
        "anthropic": get_anthropic_provider,
        "cohere": get_cohere_provider,
    }

    llm_provider = llm_strategy["openai"]
    llm = llm_provider()

    logger.info(f"Using {llm}")

    # Get input configuration from environment variables
    input_source = os.environ.get("INPUT_SOURCE")

    # Configure input handler
    if input_source == "api":
        api_url = os.environ.get("API_URL")
        api_key = os.environ.get("API_KEY")
        if not api_url:
            logger.error("API_URL environment variable is not set")
            return
        logger.info("Using API input handler")
        input_handler = get_input_handler(
            input_source, api_url=api_url, api_key=api_key
        )
    else:
        # Fallback to file input if API is not configured
        logger.info("Using File input handler")
        input_handler = get_input_handler(
            "file", file_path="src/client-exports/smith_smith.json"
        )

    try:
        user_data: str = preprocess_roadmap_output(input_handler.get_input())
    except Exception as e:
        logger.error(f"Error preprocessing user data: {e}")
        return

    # The following code block is used to create the elements needed for RAG:
    # embedding model, vector_store, user_vector, relevant_rules.
    # The vector_store is generated using the rules_ingestor.py script along with a rules.json file.

    """
    embedding_model = EmbeddingModel()

    try:
        vector_store = load_vector_store("rag_elements/rules_vector_store")
    except FileNotFoundError as e:
        logger.error(f"Error loading vector store: {e}")
        return

    user_vector = embed_user_data(embedding_model, user_data)
    relevant_rules = search_relevant_rules(vector_store, user_vector)

    context = f"User Data:\n{user_data}\n\nRelevant Rules:\n" + "\n\n".join(
        relevant_rules
    )
    """

    context = f"User Data:\n{user_data}\n"

    query = """
    Based on the provided user data for both the primary beneficiary and spouse, and the relevant Social Security rules, please provide:
    1. A summary of both individuals' work history and earnings in the form of a table with five columns: individual, total years worked, total lifetime earnings, primary insurance amount, and average annual earnings.
    2. An analysis of their estimated Social Security benefits, including any spousal benefits they might be eligible for.
    3. Recommendations for optimizing their Social Security benefits as a couple. Be extremely detailed whenever possible, including referencing the source of your information. If you are recommending strategies, please detail them in procedural form so that they can be followed easily.
    4. Any insights related to their dependents, if any.
    6. Note any specific rules that you are referencing in your analysis.

    Please ensure that the output is in proper HTML, so that the output can be displayed as a web page.
    The output should have all elements needed so that it could be displayed correctly by any modern browser.
    """

    analysis_result = analyze_with_llm(llm, query, context)
    validated: tuple = validate_llm_html(analysis_result)

    if validated[0] is True:
        logger.info("HTML was validated!")
        output_handler = get_output_handler(output_source="console")
        output_handler.process_output(analysis_result)
    else:
        logger.error("HTML Validation failed. LLM returned invalid html.")
        logger.error(validated[1])

    logger.info("Main function completed")


if __name__ == "__main__":
    main()
