from network.protocol import Request, Response
from network.encryption.diffie_hellman import DiffieHellmanState
from database.database import Database
from typing import Callable
from .models import User
from network.data import Data


def register(request: Request) -> bool:
    return "username" in request.payload and "password" in request.payload


def login(request: Request) -> bool:
    return "username" in request.payload and "password" in request.payload


def wishlist_product(request: Request) -> bool:
    return "id" in request.payload


def products(request: Request) -> bool:
    return "amount" in request.params and "page" in request.params


def handshake(request: Request, state: DiffieHellmanState) -> bool:
    if state == DiffieHellmanState.INITIALIZING:
        return "encryptionToken" in request.payload

    elif state == DiffieHellmanState.EXCHANGING_KEYS:
        return "publicKey" in request.payload and "encryptionToken" in request.payload


def authenticated(handler: Callable[[Data], Response]):
    def wrapper(data: Data):
        if not data.request.headers.get("token"):
            return Response.error("Not Authenticated")

        user = (
            Database.get_instance()
            .execute(
                "SELECT * FROM users WHERE token = ?",
                (data.request.headers["token"],),
            )
            .fetch_one()
        )

        if user == None:
            return Response.error("Not Authenticated")

        data.user = User.from_database(user)

        return handler(data)

    return wrapper
