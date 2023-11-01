import socket
from config import Config


class Communication:
    @staticmethod
    def getData(clientSocket: socket.socket) -> str:
        result = ""

        # for preventing dDoS attacks
        clientSocket.settimeout(Config.SOCKET_INPUT_TIMEOUT)

        while True:
            try:
                chunk = clientSocket.recv(1024)
            except socket.timeout:
                break

            if not chunk:
                break

            result += chunk.decode()

            if "\r\n\r\n" in result:
                break

        return result
