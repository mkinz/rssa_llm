from flask import Flask, request, jsonify
from flask.logging import default_handler
from logging_config import setup_logging
from valid_html import validate_llm_html
from llm_interface import (
    OpenAIProvider,
    CohereAIProvider,
    AnthropicAIProvider,
)
from roadmap_output_ingestor import preprocess_roadmap_output
from logging_config import get_logger
from html_cleaner import strip_newlines_from_html

from config_manager import ConfigManager
from dotenv import load_dotenv

# set environment vars
load_dotenv()

# set global configuration
config_manager = ConfigManager()

app = Flask(__name__)
app.logger.removeHandler(default_handler)
logger = get_logger(__name__)


def get_openai_provider():
    return OpenAIProvider(config_manager)


def get_anthropic_provider():
    return AnthropicAIProvider(config_manager)


def get_cohere_provider():
    return CohereAIProvider(config_manager)


llm_strategy = {
    "openai": get_openai_provider,
    "anthropic": get_anthropic_provider,
    "cohere": get_cohere_provider,
}
llm_provider = llm_strategy[config_manager.llm_provider_name]
logger.debug(f"Using LLM provider: {llm_provider}")
llm = llm_provider()


@app.route("/process", methods=["POST"])
def process_data():
    try:
        logger.debug(f":Received request data: {request.data}")

        user_data = request.json
        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        preprocessed_data = preprocess_roadmap_output(user_data)
        context = f"User Data:\n{preprocessed_data}\n"

        query = """
        Based on the provided user data for both the primary beneficiary and spouse, and the relevant Social Security rules, please provide:
        1. A summary of both individuals' work history and earnings in the form of a table with five columns: individual, total years worked, total lifetime earnings, primary insurance amount, and average annual earnings.
        2. An analysis of their estimated Social Security benefits, including any spousal benefits they might be eligible for.
        3. Recommendations for optimizing their Social Security benefits as a couple. Be extremely detailed whenever possible, including referencing the source of your information. If you are recommending strategies, please detail them in procedural form so that they can be followed easily.
        4. Any insights related to their dependents, if any.
        5. Note any specific rules that you are referencing in your analysis.

        Important: 
        - Provide your response as a complete, properly formatted HTML document, including <!DOCTYPE html>, <html>, <head>, and <body> tags.
        - Minimize the use of newline characters. Only use them where necessary for HTML structure (e.g., between major elements like <head> and <body>).
        - Do not include any markdown formatting or code block syntax.
        - Ensure all tags are properly closed and the HTML is valid.
        - Use appropriate semantic HTML5 tags where possible (e.g., <header>, <main>, <section>, <article>).
        """

        logger.info("Performing LLM analysis now...")
        analysis_result = llm.analyze(query, context)
        cleaned_results = strip_newlines_from_html(analysis_result)

        logger.info("Performing HTML validation now...")
        validated, validation_message = validate_llm_html(cleaned_results)

        if validated:
            logger.info("HTML was validated!")
            return jsonify({"status": "success", "html_report": cleaned_results})
        else:
            logger.error(f"HTML Validation failed: {validation_message}")
            return jsonify(
                {
                    "status": "error",
                    "message": "HTML validation failed",
                    "details": validation_message,
                    "partial_response": validation_message[:1000],
                }
            ), 500

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify(
            {
                "status": "error",
                "message": "An error occurred while processing the request",
                "details": str(e),
            }
        ), 500


if __name__ == "__main__":
    setup_logging()
    app.run(host=config_manager.host, port=int(config_manager.port), debug=False)
