from network.server import Server
from config import Config
import endpoints

if __name__ == "__main__":
    server = Server(
        host=Config.HOST,
        port=Config.PORT,
        timeout=Config.SOCKET_TIMEOUT,
    )

    server.start()

    print("Server started!")
