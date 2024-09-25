import pytest
from input_handler import FileInputHandler, APIInputHandler


# FileInputHandler Tests
def test_file_input_handler_init_with_valid_path():
    handler = FileInputHandler("valid_path.json")
    assert handler.file_path == "valid_path.json"


def test_file_input_handler_init_with_empty_path():
    with pytest.raises(ValueError):
        FileInputHandler("")


def test_file_input_handler_init_with_non_string_path():
    with pytest.raises(TypeError):
        FileInputHandler(123)


# APIInputHandler Tests
def test_api_input_handler_init_with_valid_url():
    handler = APIInputHandler("https://api.example.com")
    assert handler.api_url == "https://api.example.com"
    assert handler.api_key is None


def test_api_input_handler_init_with_valid_url_and_api_key():
    handler = APIInputHandler("https://api.example.com", "test_key")
    assert handler.api_url == "https://api.example.com"
    assert handler.api_key == "test_key"


def test_api_input_handler_init_with_empty_url():
    with pytest.raises(ValueError):
        APIInputHandler("")


def test_api_input_handler_init_with_non_string_url():
    with pytest.raises(TypeError):
        APIInputHandler(123)


def test_api_input_handler_init_with_invalid_url_format():
    with pytest.raises(ValueError):
        APIInputHandler("not_a_valid_url")
