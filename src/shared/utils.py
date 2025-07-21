import requests


def ping_resource(url: str) -> int:
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except Exception as e:
        return f"Error: {e}"
