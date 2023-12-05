from httpLib.server import Server
from httpLib.client import Client
from httpLib.protocol import Request, Response
from config import Config
import time


def handleClient(request: Request, client: Client):
    print("Client connected from", client.clientAddress)

    response = Response(
        content=f"The time is: {time.time()}", statusCode=Response.StatusCode.NOT_FOUND
    )
    response.setHeader("CTF", Config.CTF_FLAG)

    client.send(response)


if __name__ == "__main__":
    server = Server(
        handleClient,
        host=Config.HOST,
        port=Config.PORT,
        timeout=Config.SOCKET_TIMEOUT,
    )

    server.start()
