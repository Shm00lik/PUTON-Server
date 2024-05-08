from enum import Enum
from network.encryption.AES import AES
import json


class Request:
    class RequestMethod(Enum):
        GET = "GET"
        POST = "POST"
        PUT = "PUT"
        DELETE = "DELETE"
        UNKNOWN = "UNKNOWN"
        OPTIONS = "OPTIONS"

        @staticmethod
        def fromRequestData(requestData: str):
            mapper: dict = {v.value: v for v in Request.RequestMethod}

            if requestData.split(" ")[0] not in mapper:
                return Request.RequestMethod.UNKNOWN

            return mapper[requestData.split(" ")[0]]

    def __init__(self, data: str) -> None:
        self.splittedData = data.split("\r\n")

        self.method: Request.RequestMethod = Request.RequestMethod.UNKNOWN
        self.url: list[str] = [""]
        self.params: dict[str, str] = {}
        self.body: str = ""
        self.headers: dict[str, str] = {}
        self.payload: dict[str, str] = {}

        if len(self.splittedData) < 2:
            return

        self.parse()

    def parse(self) -> None:
        self.method = self.getMethod()
        self.url = self.getUrl()
        self.params = self.getParams()
        self.body = self.getBody()
        self.headers = self.getHeaders()
        self.payload = self.getPayload()

    def getMethod(self) -> RequestMethod:
        return Request.RequestMethod.fromRequestData(self.splittedData[0])

    def getUrl(self) -> list[str]:
        return self.splittedData[0].split(" ")[1].split("?")[0].split("/")[1:]

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
        if self.method != Request.RequestMethod.POST:
            return {}

        try:
            return json.loads(self.body)
        except:
            return {}

    def __str__(self) -> str:
        return str(self.splittedData)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattribute__(self, __name: str):
        return super().__getattribute__(__name)


class Response:
    """
    This class is responsible for creating a response to the client.
    """

    class StatusCode(Enum):
        OK = 200
        CREATED = 201
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        NOT_FOUND = 404
        CONFLICT = 409
        INTERNAL_SERVER_ERROR = 500

        @staticmethod
        def fromInt(statusCode: int):
            mapper: dict = {v.value: v for v in Response.StatusCode}

            if statusCode not in mapper:
                return Response.StatusCode.INTERNAL_SERVER_ERROR

            return mapper[statusCode]

        def __str__(self) -> str:
            return str(self.value) + " " + self.name.replace("_", " ").title()

        def __bool__(self) -> bool:
            return str(self.value).startswith("2")

    class ContentType(Enum):
        TEXT = "text"
        JSON = "json"

    def __init__(
        self,
        content: str | dict = "",
        contentType: ContentType = ContentType.TEXT,
        statusCode: StatusCode = StatusCode.OK,
        headers: dict[str, str] = {},
        key: str = "",
    ) -> None:
        self.headers: dict[str, str] = headers
        self.content: str = ""
        self.key = key
        self.setContent(content, contentType)

        self.statusCode: Response.StatusCode = statusCode

    def setContent(
        self, content: str | dict | list, contentType: ContentType = ContentType.TEXT
    ) -> "Response":
        if contentType == Response.ContentType.JSON:
            self.setHeader("Content-Type", "application/json")
            self.content = json.dumps(content)

        else:
            if isinstance(content, dict) or isinstance(content, list):
                return self.setContent(content, Response.ContentType.JSON)

            self.setHeader("Content-Type", "text/plain")
            self.content = str(content)

        if len(self.content) > 0:
            self.setHeader("Content-Length", str(len(self.content)))

        return self

    def setHeader(self, key: str, value: str) -> "Response":
        self.headers[key] = value

        return self

    def setStatusCode(self, statusCode: StatusCode) -> "Response":
        self.statusCode = statusCode

        return self

    def generate(self) -> str:
        self.setContent(
            AES.encrypt(self.content, self.key) if self.key != "" else self.content
        )

        response: str = "HTTP/1.1 " + str(self.statusCode) + "\r\n"

        response += "\r\n".join(
            [f"{key}: {value}" for key, value in self.headers.items()]
        )

        print()

        if len(self.content) > 0:
            response += "\r\n\r\n" + self.content

        response += "\r\n"
        return response

    @staticmethod
    def error(
        message: str | dict | list, statusCode: StatusCode = StatusCode.OK
    ) -> "Response":
        return Response(
            content={"success": False, "message": message},
            contentType=Response.ContentType.JSON,
            statusCode=statusCode,
        )

    @staticmethod
    def success(
        message: str | dict | list,
        statusCode: StatusCode = StatusCode.OK,
        key: str = "",
    ) -> "Response":
        return Response(
            content={"success": True, "message": message},
            contentType=Response.ContentType.JSON,
            statusCode=statusCode,
            key=key,
        )

    def __str__(self) -> str:
        return self.generate()
