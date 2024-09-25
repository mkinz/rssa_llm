import os
import json
from abc import ABC, abstractmethod
import requests
from urllib.parse import urlparse


class InputHandler(ABC):
    @abstractmethod
    def get_input(self):
        pass


class FileInputHandler(InputHandler):
    def __init__(self, file_path):
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not file_path:
            raise ValueError("file_path cannot be empty")
        self.file_path = file_path

    def get_input(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)


class APIInputHandler(InputHandler):
    def __init__(self, api_url, api_key=None):
        if not isinstance(api_url, str):
            raise TypeError("api_url must be a string")
        if not api_url:
            raise ValueError("api_url cannot be empty")
        if not self._is_valid_url(api_url):
            raise ValueError("Invalid URL format")
        self.api_url = api_url
        self.api_key = api_key

    def get_input(self):
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.get(self.api_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()

    @staticmethod
    def _is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


def get_input_handler(input_source, **kwargs):
    if input_source == "file":
        return FileInputHandler(kwargs.get("file_path"))
    elif input_source == "api":
        return APIInputHandler(kwargs.get("api_url"), kwargs.get("api_key"))
    else:
        raise ValueError(f"Unknown input source: {input_source}")


# Usage example
if __name__ == "__main__":
    # Example usage with file input
    file_handler = get_input_handler("file", file_path="data.json")
    file_data = file_handler.get_input()
    print("File data:", file_data)

    # Example usage with API input
    api_handler = get_input_handler(
        "api", api_url="https://api.example.com/data", api_key="your-api-key"
    )
    api_data = api_handler.get_input()
    print("API data:", api_data)
