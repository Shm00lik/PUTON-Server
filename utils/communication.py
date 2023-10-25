import socket
import threading
from typing import Callable


class Communication:
    @staticmethod
    def getData(clientSocket: socket.socket) -> str:
        result = ""

        clientSocket.settimeout(0.1)

        while True:
            try:
                data = clientSocket.recv(1)
            except socket.timeout:
                break

            result += data.decode()

        return result
