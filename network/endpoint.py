from typing import Callable
from .protocol import Response, HTTPMethod
from .data import Data


class Endpoint:
    """
    Represents an endpoint with its URL pattern, HTTP method, handler function, and encryption status.
    """

    def __init__(
        self,
        url: str,
        method: HTTPMethod,
        handler: Callable[[Data], Response],
        encrypted: bool = True,
    ):
        """
        Initializes an Endpoint object.

        Args:
        - url (str): The URL pattern of the endpoint.
        - method (HTTPMethod): The HTTP method of the endpoint.
        - handler (Callable[[Data], Response]): The handler function for the endpoint.
        - encrypted (bool): Whether the endpoint requires encryption (default is True).
        """
        self.url = url
        self.method = method
        self.handler = handler
        self.encrypted = encrypted

    @staticmethod
    def default_endpoint() -> "Endpoint":
        """
        Creates a default endpoint for handling requests to the root URL with a GET method,
        responding with an error indicating "Not Found".

        Returns:
        - Endpoint: A default endpoint instance.
        """
        return Endpoint("/", HTTPMethod.GET, lambda _: Response.error("Not Found"))

    def __str__(self):
        return f"{self.method} {self.url} {self.encrypted} {self.handler.__name__}"
