import os
import yaml
from logging_config import get_logger

logger = get_logger(__name__)


class LLMConfigManager:
    def __init__(self, config_path="src/run/llm_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        logger.info("Using LLM Config manager")

    def _load_config(self):
        with open(self.config_path, "r") as f:
            logger.info(f"Loaded config from path: {self.config_path}")
            return yaml.safe_load(f)

    def get_api_key(self, llm_name):
        try:
            logger.info("Loading api key")
            return os.environ.get(f"{llm_name.upper()}_API_KEY")
        except ValueError:
            raise ValueError(
                f"API key for {llm_name} not found. Ensure the secret {llm_name.lower()}_api_key is set."
            )

    def get_llm_config(self, llm_name):
        if llm_name not in self.config:
            raise ValueError(
                f"Configuration for {llm_name} not found in the config file."
            )
        logger.info(f"Using llm config for: {self.config[llm_name]}")
        return self.config[llm_name]

    def get_available_llms(self):
        return list(self.config.keys())
