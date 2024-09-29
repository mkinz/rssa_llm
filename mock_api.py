import requests
import json
import argparse


def get_sample_data(path_to_client_data: str):
    with open(path_to_client_data, "r") as raw_json_data:
        json_data = json.load(raw_json_data)
    return json_data


def send_request(url, data):
    """Send a POST request to the specified URL with the given data."""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending request: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Mock API client for testing.")
    parser.add_argument(
        "--url", default="http://localhost:5050/process", help="URL of the API endpoint"
    )
    parser.add_argument("--input", help="RSSA Roadmap json data")
    parser.add_argument("--output", help="File to save the response")
    args = parser.parse_args()

    sample_data = get_sample_data(args.input)
    print(f"Sending request to {args.url}")
    response = send_request(args.url, sample_data)

    if response:
        print("Response received:")
        print(json.dumps(response, indent=2))

        if args.output:
            with open(args.output, "w") as f:
                json.dump(response, f, indent=2)
            print(f"Response saved to {args.output}")
    else:
        print("No response received.")


if __name__ == "__main__":
    main()
    # python mock_api.py --url http://localhost:5050/process --output response.json
