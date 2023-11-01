import socket
import utils.protocol as protocol
from utils.communication import Communication
import time
import threading
import cv2

cap = cv2.VideoCapture(0)
latest = b""


def handle_request(client_socket, clientAddress):
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

    response = protocol.Response(
        headers={
            "Content-Type": "multipart/x-mixed-replace; boundary=frame\r\r\n\n",
        },
    )

    client_socket.sendall(response.generate().encode())

    # print(response)

    x = 0

    while True:
        data = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + latest + b""

        client_socket.sendall(data)

        x += 1

        print("Sent ", x)
        time.sleep(0)

    # print(response)

    client_socket.close()

    end = time.time()

    print(f"Request took {end - start} seconds")


def image():
    global latest

    while True:
        ret, frame = cap.read()
        latest = cv2.imencode(".jpg", frame)[1].tobytes()


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen(10)

    print("Listening on port 3339...")

    threading.Thread(target=image).start()

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
