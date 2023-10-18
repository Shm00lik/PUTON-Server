import socket
import utils.protocol as protocol


def handle_request(client_socket):
    request_data = client_socket.recv(1024)
    r = protocol.Request(request_data.decode())

    print("body", r.body)
    print("headers", r.headers)
    print("method", r.method)
    print("params", r.params)
    print("payload", r.payload)
    print("url", r.url)

    response = protocol.Response.createResponse("Success")
    print(response)
    client_socket.sendall(response.encode())

    client_socket.close()


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 3339))
    server_socket.listen(1)

    print("Listening on port 8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        handle_request(client_socket)


if __name__ == "__main__":
    run_server()
