from httpLib.server import Server
from httpLib.client import Client
from httpLib.protocol import Request, Response
import socket
from config import Config


def handleClient(request: Request, client: Client):
    print("Client connected from", client.clientAddress)

    response = Response(content="Hello, World!")
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
