import json


class SearchSettings:
    def __init__(self, query_url, bearer_token, headers=None, body=None):
        self.query_url = query_url
        self.bearer_token = bearer_token
        self.headers = headers if headers is not None else []
        self.body = body if body is not None else {}

    def add_header(self, key, value):
        """
        Add a header to the headers list.

        Args:
            key (str): The header key.
            value (str): The header value.
        """
        self.headers.append((key, value))

    def remove_header(self, key):
        """
        Remove a header from the headers list.

        Args:
            key (str): The header key to remove.
        """
        self.headers = [header for header in self.headers if header[0] != key]

    def update_body(self, new_body):
        """
        Update the JSON body.

        Args:
            new_body (dict): The new JSON body to update.
        """
        self.body.update(new_body)

    def set_body_from_json_file(self, file_path):
        """
        Read JSON data from a file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            dict: The JSON data read from the file.
        """
        with open(file_path, 'r') as file:
            self.update_body(json.load(file))


# Example usage:
settings = SearchSettings("https://example.com/api/search", "my_bearer_token")
settings.add_header("Content-Type", "application/json")
settings.add_header("User-Agent", "MyApp/1.0")
settings.update_body({"query": "example"})
