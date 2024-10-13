from abc import ABC, abstractmethod
from os import system
from typing import Any

import anthropic
import cohere
from openai import OpenAI

from src.config_manager import ConfigManager
from src.logging_config import get_logger


logger = get_logger(__name__)


class BaseAIProvider(ABC):
    def __init__(self, config_manager: ConfigManager):
        self.manager = config_manager
        self.llm_provider = self.manager.llm_provider_name
        self.api_key = self.manager.api_key
        self.model = self.manager.model
        self.llm_config = self.manager.llm_config
        self.client = self._create_client()
        logger.debug("Instantiated BaseAIProvider class")

    @abstractmethod
    def _create_client(self) -> Any:
        pass

    @abstractmethod
    def _send_request(self, messages) -> Any:
        pass

    def _create_messages(self, system_content, user_content):
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ]

    def analyze(self, query, context):
        system_content = (
            "You are a helpful assistant that analyzes social security data."
        )
        user_content = f"""
        Analyze the following social security data and provide insights:
        Context: {context}
        Query: {query}
        """
        messages = self._create_messages(system_content, user_content)
        req = self._send_request(messages)
        # return the output, plus the count of input and output chars for token approximation
        return req, len(system_content + user_content), len(req)


class OpenAIProvider(BaseAIProvider):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        logger.debug("Instantiated OpenAIProvider class")

    def _create_client(self):
        return OpenAI(api_key=self.api_key)

    def _send_request(self, messages):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content


class CohereAIProvider(BaseAIProvider):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def _create_client(self) -> Any:
        return cohere.Client(api_key=self.api_key)

    def _send_request(self, messages) -> Any:
        formatted_message = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in messages]
        )
        response = self.client.chat(
            message=formatted_message,
        )

        return response.text


class AnthropicAIProvider(BaseAIProvider):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def _create_client(self) -> Any:
        return anthropic.Anthropic(api_key=self.api_key)

    def _send_request(self, messages):
        system_message = next(
            (msg["content"] for msg in messages if msg["role"] == "system"), None
        )
        user_messages = [msg for msg in messages if msg["role"] == "user"]

        logger.debug(
            f"Sending request to Anthropic API. System message: {system_message}"
        )
        logger.debug(f"User messages: {user_messages}")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.manager.llm_config["max_tokens"],
                temperature=self.manager.llm_config["temperature"],
                system=system_message,
                messages=user_messages,
            )

            logger.debug(f"Received response from Anthropic API: {response}")

            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                logger.warning("No content found in Anthropic API response")
                return "No content found in response"
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
