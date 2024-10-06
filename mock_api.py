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


def check_health(url):
    """Send a GET request to the /healthz endpoint."""
    try:
        response = requests.get(f"{url}/healthz", timeout=5)
        response.raise_for_status()
        print(f"Health check status code: {response.status_code}")
        return response.status_code
    except requests.ConnectionError:
        print("Error: Unable to connect to the server. Is it running?")
        return None
    except requests.Timeout:
        print(
            "Error: Request timed out. The server might be overloaded or not responding."
        )
        return None
    except requests.RequestException as e:
        print(f"Error checking health: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred during health check: {e}")
        return None


def check_readiness(url):
    """Send a GET request to the /ready endpoint."""
    try:
        response = requests.get(f"{url}/ready", timeout=5)
        response.raise_for_status()
        print(f"Readiness check status code: {response.status_code}")
        return response.status_code
    except requests.ConnectionError:
        print("Error: Unable to connect to the server. Is it running?")
        return None
    except requests.Timeout:
        print(
            "Error: Request timed out. The server might be overloaded or not responding."
        )
        return None
    except requests.RequestException as e:
        print(f"Error checking readiness: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred during health check: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Mock API client for testing.")
    parser.add_argument(
        "--url", default="http://localhost:5050/process", help="URL of the API endpoint"
    )
    parser.add_argument("--input", help="RSSA Roadmap json data")
    parser.add_argument("--output", help="File to save the response")
    parser.add_argument("--healthz", action="store_true", help="Perform a health check")
    parser.add_argument(
        "--ready", action="store_true", help="Perform a readiness check"
    )
    args = parser.parse_args()

    if args.healthz:
        check_health(args.url)
    elif args.ready:
        check_readiness(args.url)
    else:
        if not args.input:
            print("Error: --input is required to process data")
            return

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
    # python mock_api.py --url http://localhost:5050/process --output response.json --input src/client-exports/hall_munster.json
