import socket
import utils.protocol as protocol
from utils.communication import Communication
import time
import threading


def handle_request(client_socket: socket.socket, clientAddress: socket.socket):
    print(" -------------- ")

    start = time.time()
    request_data = Communication.getData(client_socket)
    # request_data = client_socket.recv(1024).decode()

    print(len(request_data))

    print(request_data[:100])
    r = protocol.Request(request_data)
    # print("body", r.body)
    # print("headers", r.headers)
    # print("method", r.method)
    # print("params", r.params)
    # print("payload", r.payload)
    # print("url", r.url)
    if r.url != "/":
        client_socket.close()
        return

    response = protocol.Response(content='<img src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAAtJREFUGFdjYAACAAAFAAGq1chRAAAAAElFTkSuQmCC" >')
    response.setHeader("Content-Type", "text/html")

    # print(response)

    client_socket.sendall(response.generate().encode())

    client_socket.close()

    end = time.time()

    print(f"Request took {end - start} seconds")


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 1690))
    server_socket.listen(10)

    print("Listening on port 3339...")

    while True:
        client_socket, client_address = server_socket.accept()

        threading.Thread(
            target=handle_request,
            args=(
                client_socket,
                client_address,
            ),
        ).start()


if __name__ == "__main__":
    run_server()
