from enum import Enum
import utils.utils as utils
import json


class HTTPMethod(Enum):
    """
    An enumeration representing HTTP methods.
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    UNKNOWN = "UNKNOWN"
    OPTIONS = "OPTIONS"

    @staticmethod
    def from_raw(request: str):
        """
        Extracts the HTTP method from a raw HTTP request string.

        Args:
        - request (str): The raw HTTP request string.

        Returns:
        - RequestMethod: The extracted HTTP method.
        """
        lines = request.split("\r\n")
        method = lines[0].split(" ")[0]
        return HTTPMethod(method)


class Request:
    """
    A class representing an HTTP request.
    """

    def __init__(
        self,
        method: HTTPMethod = HTTPMethod.UNKNOWN,
        url: str = "",
        params: dict[str, str] = {},
        path_variables: list[str] = [],
        body: str = "",
        headers: dict[str, str] = {},
        payload: dict[str, str] = {},
    ):
        self.method = method
        self.url = url
        self.params = params
        self.path_variables = path_variables
        self.body = body
        self.headers = headers
        self.payload = payload

    @staticmethod
    def from_raw(request: str) -> "Request":
        """
        Creates a Request object from a raw HTTP request string.

        Args:
        - request (str): The raw HTTP request string.

        Returns:
        - Request: The parsed Request object.
        """

        lines = request.split("\r\n")
        method = HTTPMethod.from_raw(request)
        url = lines[0].split(" ")[1]

        # Parse path variables
        path_variables = url[1:].split("/")

        headers = {}
        params = {}
        payload = {}
        body = ""

        # Parse headers
        for line in lines[1:]:
            if line == "":  # means that we reached to \r\n\r\n
                break

            key, value = line.split(": ", 1)
            headers[key] = value.strip()

        # Parse URL parameters
        if "?" in url:
            url, query_string = url.split("?", 1)
            params = dict(param.split("=") for param in query_string.split("&"))

        # Parse body and payload for POST requests (assuming JSON)
        if method == HTTPMethod.POST and lines[-1]:
            body = lines[-1]

            if utils.is_json(body):
                payload = json.loads(body)

        return Request(
            method=method,
            url=url,
            params=params,
            path_variables=path_variables,
            headers=headers,
            body=body,
            payload=payload,
        )


class Response:
    """
    A class representing an HTTP response.
    """

    def __init__(self, headers: dict[str, str] = {}, body: str | dict = "") -> None:
        self.headers = headers
        self.body = json.dumps(body)

    def set_header(self, key: str, value: str):
        """
        Sets a header in the response.

        Args:
        - key (str): The header key.
        - value (str): The header value.
        """
        self.headers[key] = value

    def to_http_string(self) -> str:
        """
        Convert the Response object to an HTTP response string.

        Returns:
        - str: The HTTP response string.
        """
        self.set_header("Content-Length", str(len(self.body)))
        self.set_header("Content-Type", "application/json")

        header_lines = "\r\n".join(
            [f"{key}: {value}" for key, value in self.headers.items()]
        )

        response_string = f"HTTP/1.1 200 OK\r\n{header_lines}\r\n\r\n{self.body}"
        return response_string

    @staticmethod
    def error(data: str | dict | list) -> "Response":
        """
        Creates an error response.

        Args:
        - data (str | dict | list): The error data.

        Returns:
        - Response: The error response.
        """
        if isinstance(data, dict):
            return Response(
                body={"success": False, **data},
            )

        if isinstance(data, list):
            return Response(
                body={"success": False, "data": data},
            )

        return Response(
            body={"success": False, "message": data},
        )

    @staticmethod
    def success(data: str | dict | list) -> "Response":
        """
        Creates a success response.

        Args:
        - data (str | dict | list): The success data.

        Returns:
        - Response: The success response.
        """
        if isinstance(data, dict):
            return Response(
                body={"success": True, **data},
            )

        if isinstance(data, list):
            return Response(
                body={"success": True, "data": data},
            )

        return Response(
            body={"success": True, "message": data},
        )

    def __str__(self) -> str:
        return self.to_http_string()
