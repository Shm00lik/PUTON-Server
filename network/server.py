import socket
import threading

from .endpoint import Endpoint
from .router import Router
from .protocol import Request, Response
from .client import Client
from .data import Data
from database.database import Database
from .encryption.AES import AES


class Server:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3339,
        backlog: int = 5,
        max_clients: int = 100,
        timeout: float = 1.0,
    ):
        if host == "" or port < 1000:
            return

        self.host: str = host
        self.port: int = port
        self.backlog: int = backlog

        self.server_thread: threading.Thread = threading.Thread(target=self.run)
        self.max_clients: int = max_clients
        self.clients: list[Client] = []
        self.threads: list[threading.Thread] = []
        self.socket: socket.socket = socket.socket()

        self.should_run: bool = True
        self.has_stopped: bool = False

        self.timeout = timeout

        self.socket.settimeout(timeout)

        self.encryptions: dict[int, str] = {}

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.backlog)

            self.server_thread.start()
        except Exception as e:
            print("Error while trying to start server: \n" + str(e))

    def run(self) -> None:
        while self.should_run:
            if len(self.clients) > self.max_clients:
                print("Max clients reached, waiting for clients to disconnect...")
                break

            try:
                self.accept()
            except socket.timeout:
                pass

        if not self.has_stopped:
            self.stop()

    def accept(self) -> None:
        client_socket, client_address = self.socket.accept()

        client = Client(client_socket, client_address)
        self.clients.append(client)

        t = threading.Thread(target=self.handle_client, args=(client,))

        self.threads.append(t)
        t.start()

    def stop(self):
        self.should_run = False
        self.has_stopped = True

        for thread in self.threads:
            thread.join()

        self.socket.close()

    def handle_client(self, client: Client) -> None:
        request_data = client.get_data(self.timeout)

        if request_data == "":
            client.close()
            return

        request = Request.from_raw(request_data)

        endpoint = Router.get_endpoint(request)

        print(
            f"Request from {client.client_address}. METHOD: {request.method}. URL: {request.url}"
        )

        response = self.before_handle(request, endpoint)
        response = endpoint.handler(
            Data(request, Database.get_instance(), client, self)
        )
        response = self.after_handle(request, response, endpoint)

        client.send(response)

        self.clients.remove(client)
        client.close()

    def before_handle(self, request: Request, endpoint: Endpoint):
        if endpoint.encrypted:
            encryption_token = int(request.headers.get("encryptionToken") or 0)

            if not encryption_token or not self.already_encrypted(encryption_token):
                return

            encryption_key = self.get_encryption_key(encryption_token)

            request.body = AES.decrypt(request.body, encryption_key)

    def after_handle(
        self, request: Request, response: Response, endpoint: Endpoint
    ) -> Response:
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Access-Control-Allow-Headers", "*")
        response.set_header("Access-Control-Allow-Methods", "*")

        if endpoint.encrypted:
            encryption_token = int(request.headers.get("encryptionToken") or 0)

            if not encryption_token or not self.already_encrypted(encryption_token):
                return Response.error("Invalid Request")

            encryption_key = self.get_encryption_key(encryption_token)

            response.body = AES.encrypt(response.body, encryption_key)

        return response

    def add_encryption(self, token: int, key: str):
        self.encryptions[token] = key

    def get_encryption_key(self, token: int) -> str:
        return self.encryptions[token]

    def already_encrypted(self, token: int) -> bool:
        return token in self.encryptions
