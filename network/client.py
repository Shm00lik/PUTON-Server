import socket
from .protocol import Response


class Client:
    def __init__(self, client_socket: socket.socket, client_address: tuple) -> None:
        self.client_socket: socket.socket = client_socket
        self.client_address: tuple = client_address

    def send(self, response: Response) -> None:
        self.client_socket.sendall(response.to_http_string().encode())

    def get_data(self, timeout: float = 1) -> str:
        result = ""

        # for preventing dDoS attacks
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
        self.client_socket.close()
