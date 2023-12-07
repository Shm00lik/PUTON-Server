from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
from typing import Callable
import json
from sqliteLib.database import Database
from sqliteLib.table import Table
import time


class BusinessLogic:
    print("Initializing database")
    db = Database(Config.DATABASE_PATH)

    usersTable = Table("users")

    @staticmethod
    def handleClient(request: Request, client: Client):
        print("Client connected from", client.clientAddress)

        response: Response | None = None

        if request.method == Request.RequestMethod.POST:
            if request.type == Request.RequestType.REGISTER:
                response = BusinessLogic.register(request)

            elif request.type == Request.RequestType.LOGIN:
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

        response.setHeader("CTF", Config.CTF_FLAG)

        client.send(response)

    @staticmethod
    def validateRequest(request: Request, function: Callable[[Request], bool]) -> bool:
        return function(request)

    @staticmethod
    def register(request: Request) -> Response:
        if not BusinessLogic.validateRequest(request, lambda r: r.payload is not None):
            return Response(
                content=json.dumps({"error": "Invalid request"}),
                statusCode=Response.StatusCode.BAD_REQUEST,
            )

        BusinessLogic.usersTable.insert(
            username=request.payload["username"],
            password=request.payload["password"],
        ).execute()

        print("Registering new user " + str(request.payload))

        return Response(content="{'msg': 'User registered successfully'}")

    @staticmethod
    def login(request: Request) -> Response:
        print("Logging in user " + str(request))

        return Response(content="'msg': 'User logged in successfully'")
