from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
from sqliteLib.database import Database
from sqliteLib.table import Table, FetchType
from enum import Enum


class RequestType(Enum):
    UNKNOWN = "unknown"

    REGISTER = "register"
    LOGIN = "login"
    DISCONNECT = "disconnect"

    @staticmethod
    def fromUrl(url: str) -> "RequestType":
        mapper: dict = {v.value: v for v in RequestType}

        if "/" not in url:
            return RequestType.UNKNOWN

        if url.split("/")[1] not in mapper:
            return RequestType.UNKNOWN

        return mapper[url.split("/")[1]]


class RequestValidator:
    @staticmethod
    def register(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def login(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload


class BusinessLogic:
    db = Database(Config.DATABASE_PATH)

    usersTable = Table("users")

    @staticmethod
    def handleClient(request: Request, client: Client):
        print("Client connected from", client.clientAddress)

        requestTpye = RequestType.fromUrl(request.url)
        response: Response | None = None

        if request.method == Request.RequestMethod.POST:
            if requestTpye == RequestType.REGISTER:
                response = BusinessLogic.register(request)

            elif requestTpye == RequestType.LOGIN:
                response = BusinessLogic.login(request)

        elif request.method == Request.RequestMethod.GET:
            response = Response(
                content="Hello, World!",
                statusCode=Response.StatusCode.OK,
            )

        if response is None:
            response = Response(
                content="Please check your request and try again",
                statusCode=Response.StatusCode.NOT_FOUND,
            )

        # response.setHeader("CTF", Config.CTF_FLAG)
        response.setHeader("Access-Control-Allow-Origin", "*")

        print(response)
        client.send(response)

    @staticmethod
    def register(request: Request) -> Response:
        if not RequestValidator.register(request):
            return Response.error("Invalid request")

        BusinessLogic.usersTable.insert(
            username=request.payload["username"],
            password=request.payload["password"],
        ).execute()

        return Response.success("User registered successfully")

    @staticmethod
    def login(request: Request) -> Response:
        if not RequestValidator.login(request):
            return Response.error("Invalid request")

        return Response(
            content={
                "success": True,
                "message": str(
                    BusinessLogic.usersTable.select("*")
                    .where(
                        username=request.payload["username"],
                        password=request.payload["password"],
                    )
                    .execute(fetchType=FetchType.ONE)
                ),
            },
            contentType=Response.ContentType.JSON,
        )
