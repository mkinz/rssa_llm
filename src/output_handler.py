from abc import ABC, abstractmethod


class OutputHandler(ABC):
    @abstractmethod
    def process_output(self, analysis_result: str):
        pass


class ConsoleOutputHandler(OutputHandler):
    def process_output(self, analysis_result: str):
        print(analysis_result)


class APIOutputHandler(OutputHandler):
    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def process_output(self, analysis_result: str):
        # Implement API call logic here
        print(f"Sending output to API endpoint: {self.api_endpoint}")
        # You would typically use a library like requests to make the API call
        # requests.post(self.api_endpoint, data=analysis_result)


class FileOutputHandler(OutputHandler):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def process_output(self, analysis_result: str):
        with open(self.file_path, "w") as f:
            f.write(analysis_result)
        print(f"Output saved to file: {self.file_path}")


def get_output_handler(output_source: str, **kwargs):
    if output_source == "console":
        return ConsoleOutputHandler()
    if output_source == "api":
        return APIOutputHandler(kwargs.get("api_endpoint"))
    if output_source == "file":
        return FileOutputHandler(kwargs.get("file_path"))
    else:
        raise ValueError(f"Unknown input source: {output_source}")
