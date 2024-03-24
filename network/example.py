from server import Server
from client import Client
import protocol


def handleClient(request: protocol.Request, client: Client):
    print(f"New client connected: {client.clientAddress}")
    print(f"Request url: {request.url}")

    client.send(protocol.Response(content="Hello!"))


server = Server(handleClient)
server.start()

input("Press enter to stop server...")
server.stop()
