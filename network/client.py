import socket
from .protocol import Response


class Client:
    def __init__(self, clientSocket: socket.socket, clientAddress: tuple) -> None:
        self.clientSocket: socket.socket = clientSocket
        self.clientAddress: tuple = clientAddress

    def send(self, response: Response) -> None:
        self.clientSocket.sendall(response.generate().encode())

    def getData(self, timeout: float = 1) -> str:
        result = ""

        # for preventing dDoS attacks
        self.clientSocket.settimeout(timeout)

        while True:
            try:
                chunk = self.clientSocket.recv(1024)
            except socket.timeout:
                break

            if not chunk:
                break

            result += chunk.decode()

            if "\r\n\r\n" in result:
                break

        return result

    def close(self):
        self.clientSocket.close()
