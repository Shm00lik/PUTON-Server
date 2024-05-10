from typing import Callable
from .protocol import Request, Response, HTTPMethod
from .endpoint import Endpoint
from .data import Data


class Router:
    """
    A router class to handle routing of HTTP requests to their respective handlers.
    """

    endpoints: list[Endpoint] = []

    @classmethod
    def route(cls, url: str, method: HTTPMethod, encrypted: bool = True):
        """
        A decorator to register a route with the router.

        Args:
        - url (str): The URL pattern to match against.
        - method (HTTPMethod): The HTTP method of the request.
        - encrypted (bool): Whether the route requires encryption (default is True).

        Returns:
        - Callable[[Data], Response]: The decorated function.
        """

        def decorator(func: Callable[[Data], Response]) -> Callable[[Data], Response]:
            if url.startswith("/"):
                cls.endpoints.append(Endpoint(url, method, func, encrypted))
            else:
                cls.endpoints.append(Endpoint("/" + url, method, func, encrypted))

            return func

        return decorator

    @classmethod
    def get_endpoint(cls, request: Request) -> Endpoint:
        """
        Handles the incoming request by finding the appropriate endpoint and calling its handler.

        Args:
        - request (Request): The incoming request.

        Returns:
        - Endpoint: The endpoint matching the request.
        """

        filtered_endpoints = list(
            filter(lambda e: e.method == request.method, cls.endpoints)
        )

        for endpoint in filtered_endpoints:
            if cls.urls_match_pattern(endpoint.url, request.url):
                return endpoint

        return Endpoint.default_endpoint()

    @staticmethod
    def urls_match_pattern(url: str, request_url: str) -> bool:
        """
        Checks if the URL and the request URL match according to the pattern.

        Args:
        - url (str): The URL pattern to match against.
        - request_url (str): The URL from the request.

        Returns:
        - bool: True if the URLs match the pattern, False otherwise.
        """

        url_parts = url.split("/")
        request_url_parts = request_url.split("/")

        if len(url_parts) != len(request_url_parts):
            return False

        for i in range(len(url_parts)):
            if url_parts[i].startswith(":"):
                continue

            elif url_parts[i] != request_url_parts[i]:
                return False

        return True
