import socket
from config import Config
import threading


class Server:
    def __init__(self):
        self.host: str = Config.HOST
        self.port: int = Config.PORT
        self.clients: list[socket.socket] = []
        self.threads: list[threading.Thread] = []
        self.socket: socket.socket = None

    def start(self):
        try:
            self.socket = socket.socket()
        except Exception as e:
            print("Error while trying to start server: \n" + str(e))

    def accept(self) -> None:
        clientSocket, clientAddress = self.socket.accept()

        t = threading.Thread(target=self.handleClient, args=(clientSocket, clientAddress))

        self.threads.append(t)
        t.start()

    def handleClient(self, clientSocket: socket.socket, clientAddress: tuple):
        pass


    def shouldRun(self) -> bool:
        return self.socket is not None

