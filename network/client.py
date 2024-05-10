import socket
from .protocol import Response


class Client:
    """
    A class representing a client connected to a server.
    """

    def __init__(self, client_socket: socket.socket, client_address: tuple) -> None:
        """
        Initializes the Client instance.

        Args:
        - client_socket (socket.socket): The client's socket.
        - client_address (tuple): The client's address (IP address, port).
        """
        self.client_socket: socket.socket = client_socket
        self.client_address: tuple = client_address

    def send(self, response: Response) -> None:
        """
        Sends a response to the client.

        Args:
        - response (Response): The response to send.
        """
        self.client_socket.sendall(response.to_http_string().encode())

    def get_data(self, timeout: float = 1) -> str:
        """
        Receives data from the client.

        Args:
        - timeout (float): Timeout value in seconds (default is 1 second).

        Returns:
        - str: The received data as a string.
        """
        result = ""

        # Set timeout for preventing dDoS attacks
        self.client_socket.settimeout(timeout)

        while True:
            try:
                chunk = self.client_socket.recv(1024)
            except socket.timeout:
                break

            if not chunk:
                break

            result += chunk.decode()

            if "\r\n\r\n" in result:
                break

        return result

    def close(self):
        """
        Closes the client socket.
        """
        self.client_socket.close()
