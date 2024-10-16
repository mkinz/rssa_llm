import os
import yaml
from src.logging_config import get_logger

logger = get_logger(__name__)


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # implement the singleton pattern so we only ever have one instance of config manager
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, config_path="src/run/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.port = self._get_port()
        self.host = self._get_host()
        self.llm_provider_name = self._get_llm_provider()
        self.api_key = self._get_api_key(llm_provider=self.llm_provider_name)
        self.llm_config = self._get_llm_config(llm_name=self.llm_provider_name)
        self.model = self.llm_config["model"]

        logger.debug("Using LLM Config manager")
        self.initialized = True

    def _load_config(self):
        with open(self.config_path, "r") as f:
            logger.debug(f"Loaded config from path: {self.config_path}")
            return yaml.safe_load(f)

    def _get_api_key(self, llm_provider):
        try:
            logger.debug("Loading api key")
            return os.environ.get(f"{llm_provider.upper()}_API_KEY")
        except ValueError:
            raise ValueError(
                f"API key for {llm_provider} not found. Ensure the secret {llm_provider.lower()}_api_key is set."
            )

    def _get_llm_config(self, llm_name):
        if llm_name not in self.config:
            raise ValueError(
                f"Configuration for {llm_name} not found in the config file."
            )
        logger.debug(f"Using llm config for: {self.config[llm_name]}")
        return self.config[llm_name]

    def _get_port(self):
        return self.config["general"]["port"]

    def _get_llm_provider(self):
        return self.config["general"]["llm_provider"]

    def _get_host(self):
        return self.config["general"]["host"]


if __name__ == "__main__":
    manager = ConfigManager()
    print(manager.config)
    print(manager.port)
    print(manager.llm_provider_name)
    print(manager.api_key)
    print(manager.llm_config)
    print(manager.llm_config["model"])
