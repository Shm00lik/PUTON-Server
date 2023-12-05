from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
import time


class BusinessLogic:
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
    def register(request: Request) -> Response:
        print("Registering new user " + str(request.payload))

        return Response(content="{'a': 'User registered successfully'}")

    @staticmethod
    def login(request: Request) -> Response:
        print("Logging in user " + str(request))

        return Response(content="'a': 'User logged in successfully'")
