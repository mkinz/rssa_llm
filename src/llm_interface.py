from abc import ABC, abstractmethod
from typing import Any

import anthropic
import cohere
from openai import OpenAI
from dotenv import load_dotenv

from llm_config_manager import LLMConfigManager
from logging_config import get_logger


logger = get_logger(__name__)


class BaseAIProvider(ABC):
    def __init__(self, provider_name):
        load_dotenv()
        self.provider_name = provider_name
        self.manager = LLMConfigManager()
        self.config = self.manager.get_llm_config(self.provider_name)
        self.api_key = self.manager.get_api_key(self.provider_name)
        self.model = self.config["model"]
        self.client = self._create_client()
        logger.info("Instantiated BaseAIProvider class")

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
        return self._send_request(messages)


class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        super().__init__("openai")
        logger.info("Instantiated OpenAIProvider class")

    def _create_client(self):
        return OpenAI(api_key=self.api_key)

    def _send_request(self, messages):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content


class CohereAIProvider(BaseAIProvider):
    def __init__(self):
        super().__init__("cohere")

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
    def __init__(self):
        super().__init__("anthropic")

    def _create_client(self) -> Any:
        return anthropic.Anthropic(api_key=self.api_key)

    def _send_request(self, messages):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.config["max_tokens"],
            temperature=self.config["temperature"],
            messages=messages,
        )

        if response.content and len(response.content) > 0:
            return response.content[0].text
        else:
            return "No content found in response"


'''
class OllamaProvider:
    """
    Note: Ollama server must be running locally before this will work.
    commands: ollama serve
    """

    def __init__(self):
        # def __init__(self, model="gemma2:9b"):
        self.api_url = "http://localhost:11434/api/generate"
        # print(f"using {self.model}")

    def analyze(self, query, context):
        prompt = f"""
        You are a helpful assistant that analyzes social security data. Please do the following:

        Analyze the following social security data and provide insights:
        Context: {context}
        Query: {query}
        """

        payload = {"model": self.model, "prompt": prompt, "stream": False}

        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            return json.loads(response.text)["response"]
        else:
            raise Exception(f"Error from Ollama API: {response.text}")
            '''
