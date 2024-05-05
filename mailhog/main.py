import requests

from .types import Messages


class Mailhog:
    """A client for Mailhog.

    :param host: The host of the Mailhog server. Defaults to "localhost".
    :param port: The port of the Mailhog server. Defaults to 8025.

    :raises requests.exceptions.ConnectionError: If the connection to Mailhog fails.
    """

    def __init__(self, host: str = "localhost", port: int = 8025) -> None:
        self.host = host
        self.port = port

    def messages(self, start: int = 0, limit: int = 50) -> Messages:
        """Get multiple messages from Mailhog.

        :param start: The index of the first message to return, optional.
        :param limit: The maximum number of messages to return, optional, defaults to 50.

        :return: A list of messages.

        :raises requests.exceptions.HTTPError: If the request fails.
        """
        response = requests.get(
            f"http://{self.host}:{self.port}/api/v2/messages",
            params={"start": start, "limit": limit},
        )
        response.raise_for_status()

        return Messages.from_json(response.text)

    def search(
        self, query: str, kind: str = "containing", start: int = 0, limit: int = 50
    ) -> Messages:
        """Search for messages in Mailhog.

        :param query: The query to search for.
        :param kind: query kind (from/to/containing), optional, defaults to containing.
        :param start: The index of the first message to return, optional.
        :param limit: The maximum number of messages to return, optional, defaults to 50.

        :return: A list of messages.

        :raises requests.exceptions.HTTPError: If the request fails.
        """
        response = requests.get(
            f"http://{self.host}:{self.port}/api/v2/search",
            params={"query": query, "kind": kind, "start": start, "limit": limit},
        )
        response.raise_for_status()

        return Messages.from_json(response.text)

    def delete_all(self) -> None:
        """Delete all messages from Mailhog.

        :raises requests.exceptions.HTTPError: If the request fails.
        """
        response = requests.delete(f"http://{self.host}:{self.port}/api/v1/messages")
        response.raise_for_status()

    def delete(self, message) -> None:
        """Deletes given message.

        :raises requests.exceptions.HTTPError: If the request fails.
        """
        response = requests.delete(
            f"http://{self.host}:{self.port}/api/v1/messages/{message.id}"
        )
        response.raise_for_status()
