import requests


def perform_post(search_settings):
    """
    Perform an HTTP POST request with the given SearchSettings.

    Args:
        search_settings (SearchSettings): An instance of SearchSettings.

    Returns:
        dict: The JSON result of the POST request.
    """
    headers = {"Authorization": f"Bearer {search_settings.bearer_token}"}
    headers.update(search_settings.headers)

    response = requests.post(
        search_settings.query_url,
        headers=headers,
        json=search_settings.body,
        timeout=30,
    )
    response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

    return response.json()


def perform_get(query_url):
    response = requests.get(query_url, timeout=30)
    response.raise_for_status()

    return response.json()
