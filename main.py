from httpLib.server import Server
from httpLib.protocol import Request, Response
import socket
from config import Config


def handleClient(request: Request, client: socket.socket, addr: tuple):
    print("Client connected from", addr)

    response = Response()
    response.setHeader("CTF", Config.CTF_FLAG)

    client.sendall(response.generate().encode())
    client.close()


if __name__ == "__main__":
    server = Server(
        handleClient,
        host=Config.HOST,
        port=Config.PORT,
        timeout=Config.SOCKET_TIMEOUT,
    )
    server.start()
