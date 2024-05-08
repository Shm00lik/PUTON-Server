from network.protocol import Request, Response
from network.encryption.diffieHellman import DiffieHellmanState
from database.database import Database


class RequestValidator:
    @staticmethod
    def register(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def login(request: Request) -> bool:
        return "username" in request.payload and "password" in request.payload

    @staticmethod
    def wishlistProduct(request: Request) -> bool:
        return "id" in request.payload

    @staticmethod
    def products(request: Request) -> bool:
        return "amount" in request.params and "page" in request.params

    @staticmethod
    def handshake(request: Request, state: DiffieHellmanState) -> bool:
        if state == DiffieHellmanState.INITIALIZING:
            return "encryptionToken" in request.payload

        elif state == DiffieHellmanState.EXCHANGING_KEYS:
            return (
                "publicKey" in request.payload and "encryptionToken" in request.payload
            )

        return False

    @staticmethod
    def authenticated(func):
        def wrapper(request: Request):
            if "token" not in request.headers:
                return Response.error("Not Authenticated")

            user = (
                Database.getInstance()
                .execute(
                    "SELECT * FROM users WHERE token = ?", (request.headers["token"],)
                )
                .fetchOne()
            )

            if user == None:
                return Response.error("Not Authenticated")

            request.user = user

            return func(request)

        return wrapper
