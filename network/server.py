import socket
import threading
import json
import utils.utils as utils
from .endpoint import Endpoint
from .router import Router
from .protocol import Request, Response
from .client import Client
from .data import Data
from database.database import Database
from .encryption.AES import AES


class Server:
    """
    A class representing a simple HTTP server.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3339,
        backlog: int = 5,
        max_clients: int = 100,
        timeout: float = 1.0,
    ):
        """
        Initializes a Server instance.

        Args:
        - host (str): The IP address to bind the server to.
        - port (int): The port number to bind the server to.
        - backlog (int): The maximum number of pending connections.
        - max_clients (int): The maximum number of concurrent clients.
        - timeout (float): The timeout duration for socket operations.
        """
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
        """
        Starts the server by binding to the host and port and starting the main server thread.
        """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.backlog)

            self.server_thread.start()
        except Exception as e:
            print("Error while trying to start server: \n" + str(e))

    def run(self) -> None:
        """
        The main server loop that accepts incoming connections and handles them.
        """
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
        """
        Accepts an incoming connection and spawns a new thread to handle it.
        """
        client_socket, client_address = self.socket.accept()

        client = Client(client_socket, client_address)
        self.clients.append(client)

        t = threading.Thread(target=self.handle_client, args=(client,))

        self.threads.append(t)
        t.start()

    def stop(self):
        """
        Stops the server by closing all client connections and the main server socket.
        """
        self.should_run = False
        self.has_stopped = True

        for thread in self.threads:
            thread.join()

        self.socket.close()

    def handle_client(self, client: Client) -> None:
        """
        Handles a client connection by receiving and processing incoming requests.

        Args:
        - client (Client): The client connection to handle.
        """
        request_data = client.get_data(self.timeout)

        if request_data == "":
            client.close()
            return

        request = Request.from_raw(request_data)

        endpoint = Router.get_endpoint(request)

        print(
            f"Request from {client.client_address}. Method: {request.method}. URL: {request.url}"
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
        """
        Pre-processing logic before handling a request.

        Args:
        - request (Request): The incoming request.
        - endpoint (Endpoint): The matched endpoint for the request.
        """
        if endpoint.encrypted:
            encryption_token = int(request.headers.get("encryptionToken") or 0)

            if not encryption_token or not self.already_encrypted(encryption_token):
                return

            encryption_key = self.get_encryption_key(encryption_token)

            request.body = AES.decrypt(request.body, encryption_key)

            request.payload = (
                json.loads(request.body) if utils.is_json(request.body) else {}
            )

    def after_handle(
        self, request: Request, response: Response, endpoint: Endpoint
    ) -> Response:
        """
        Post-processing logic after handling a request.

        Args:
        - request (Request): The incoming request.
        - response (Response): The response generated by the endpoint handler.
        - endpoint (Endpoint): The matched endpoint for the request.

        Returns:
        - Response: The processed response.
        """
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Access-Control-Allow-Headers", "*")
        response.set_header("Access-Control-Allow-Methods", "*")

        if endpoint.encrypted:
            encryption_token = int(request.headers.get("encryptionToken") or 0)

            if not encryption_token or not self.already_encrypted(encryption_token):
                return Response.error("EncryptionToken is missing or invalid")

            encryption_key = self.get_encryption_key(encryption_token)

            response.body = AES.encrypt(response.body, encryption_key)

        return response

    def add_encryption(self, token: int, key: str):
        """
        Adds an encryption token and key pair to the server's encryption registry.

        Args:
        - token (int): The encryption token.
        - key (str): The encryption key corresponding to the token.
        """
        self.encryptions[token] = key

    def get_encryption_key(self, token: int) -> str:
        """
        Retrieves the encryption key associated with a given token.

        Args:
        - token (int): The encryption token.

        Returns:
        - str: The encryption key corresponding to the token.
        """
        return self.encryptions[token]

    def already_encrypted(self, token: int) -> bool:
        """
        Checks if a given token has already been associated with an encryption key.

        Args:
        - token (int): The encryption token.

        Returns:
        - bool: True if the token is already associated with an encryption key, False otherwise.
        """
        return token in self.encryptions
