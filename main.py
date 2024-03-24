from network.server import Server
from config import Config
from businessLogic.businessLogic import BusinessLogic

if __name__ == "__main__":
    server = Server(
        BusinessLogic.getInstance().handleClient,
        host=Config.HOST,
        port=Config.PORT,
        timeout=Config.SOCKET_TIMEOUT,
    )

    server.start()

    print("Server started!")
