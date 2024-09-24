import os
from logging_config import setup_logging
from valid_html import validate_llm_html
from llm_interface import (
    OpenAIProvider,
    CohereAIProvider,
    AnthropicAIProvider,
)
from roadmap_output_ingestor import preprocess_roadmap_output
from output_handler import get_output_handler
from input_handler import get_input_handler

logger = setup_logging()


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

    analysis_result = llm.analyze(query, context)
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
