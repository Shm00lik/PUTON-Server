from enum import Enum
from config import Config


class StatusCode(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    @staticmethod
    def fromInt(statusCode: int):
        mapper: dict = {v.value: v for v in StatusCode}

        if statusCode not in mapper:
            return StatusCode.INTERNAL_SERVER_ERROR

        return mapper[statusCode]

    def __str__(self) -> str:
        return str(self.value) + " " + self.name

    def __bool__(self) -> bool:
        return str(self.value).startswith("2")


class RequestType(Enum):
    REGISTER = "register"
    LOGIN = "login"
    DISCONNECT = "disconnect"

    UNKNOWN = "unknown"

    @staticmethod
    def fromUrl(url: str):
        mapper: dict = {v.value: v for v in RequestType}
        path = url.split("/")[1]

        if path not in mapper:
            return RequestType.UNKNOWN

        return mapper[path]


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def fromRequestData(requestData: str):
        mapper: dict = {v.value: v for v in RequestMethod}

        if requestData.split(" ")[0] not in mapper:
            return RequestMethod.UNKNOWN

        return mapper[requestData.split(" ")[0]]


class Request:
    def __init__(self, data: str) -> None:
        self.splittedData = data.split("\r\n")

        self.method = self.getMethod()
        self.url = self.getUrl()
        self.params = self.getParams()
        self.body = self.getBody()
        self.headers = self.getHeaders()
        self.payload = self.getPayload()

    def getMethod(self) -> RequestMethod:
        return RequestMethod.fromRequestData(self.splittedData[0])

    def getUrl(self) -> str:
        return self.splittedData[0].split(" ")[1].split("?")[0]

    def getParams(self) -> dict[str, str]:
        params: dict[str, str] = {}

        splitted = self.splittedData[0].split(" ")[1].split("?")

        if len(splitted) < 2:
            return params

        for param in splitted[1].split("&"):
            params[param.split("=")[0]] = param.split("=")[1]

        return params

    def getBody(self) -> str:
        return self.splittedData[-1]

    def getHeaders(self) -> dict[str, str]:
        headers: dict[str, str] = {}

        for header in self.splittedData[1:-2]:
            headers[header.split(": ")[0]] = header.split(": ")[1]

        return headers

    def getPayload(self) -> dict[str, str]:
        payload: dict[str, str] = {}

        splitted = self.getBody().split("&")

        if len(splitted) < 2:
            return payload

        for param in splitted:
            payload[param.split("=")[0]] = param.split("=")[1]

        return payload


class Response:
    """
    This class is responsible for creating a response to the client.
    """

    # A template for the response with placeholders (totally not hiding a CTF)
    HTTP_RESPONSE_TEMPLATE: str = "HTTP/1.1 -STATUS_CODE-\r\nContent-Length: -CONTENT_LENGTH-\r\nCTF: QWRtaW4gUGFzc3dvcmQ6IDY4NzQ3NDcwNzMzQTJGMkY3Nzc3NzcyRTc5NkY3NTc0NzU2MjY1MkU2MzZGNkQyRjc3NjE3NDYzNjgzRjc2M0Q3ODc2NDY1QTZBNkYzNTUwNjc0NzMw\r\n\r\n-CONTENT-"

    @staticmethod
    def createResponse(content: str) -> str:
        """
        This method creates a response with a status code of 200 (OK).

        Parameters:
            content (str): The content of the response.

        Returns:
            str: The response.
        """

        return Response.createResponseWithStatusCode(content, StatusCode.OK)

    @staticmethod
    def createResponseWithStatusCode(content: str, statusCode: StatusCode) -> str:
        """
        This method creates a response with a custom status code.

        Parameters:
            content (str): The content of the response.
            statusCode (StatusCode): The status code of the response.

        Returns:
            str: The response.
        """

        return (
            Response.HTTP_RESPONSE_TEMPLATE.replace("-STATUS_CODE-", str(statusCode))
            .replace("-CONTENT_LENGTH-", str(len(content)))
            .replace("-CONTENT-", content)
        )
