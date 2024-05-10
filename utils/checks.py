from network.protocol import Request, Response
from network.encryption.diffie_hellman import DiffieHellmanState
from database.database import Database
from typing import Callable
from .models import User
from network.data import Data


def register(request: Request) -> bool:
    """
    Validates whether the request contains the necessary payload fields for user registration.

    Args:
    - request (Request): The incoming request.

    Returns:
    - bool: True if the request contains 'username' and 'password' fields in the payload, False otherwise.
    """
    return "username" in request.payload and "password" in request.payload


def login(request: Request) -> bool:
    """
    Validates whether the request contains the necessary payload fields for user login.

    Args:
    - request (Request): The incoming request.

    Returns:
    - bool: True if the request contains 'username' and 'password' fields in the payload, False otherwise.
    """
    return "username" in request.payload and "password" in request.payload


def product(request: Request) -> bool:
    """
    Validates whether the request contains the necessary parameters for retrieving a product.

    Args:
    - request (Request): The incoming request.

    Returns:
    - bool: True if the request contains product's id and it's a number, False otherwise.
    """
    return len(request.path_variables) > 1 and (request.path_variables[1]).isdigit()


def wishlist_product(request: Request) -> bool:
    """
    Validates whether the request contains the necessary payload fields for adding a product to the wishlist.

    Args:
    - request (Request): The incoming request.

    Returns:
    - bool: True if the request contains 'id' field in the payload, False otherwise.
    """
    return "id" in request.payload


def products(request: Request) -> bool:
    """
    Validates whether the request contains the necessary parameters for retrieving products.

    Args:
    - request (Request): The incoming request.

    Returns:
    - bool: True if the request contains 'amount' and 'page' parameters, False otherwise.
    """
    return "amount" in request.params and "page" in request.params


def handshake(request: Request, state: DiffieHellmanState) -> bool:
    """
    Validates handshake requests based on the current state of Diffie-Hellman key exchange.

    Args:
    - request (Request): The incoming request.
    - state (DiffieHellmanState): The current state of Diffie-Hellman key exchange.

    Returns:
    - bool: True if the request is valid for the given state, False otherwise.
    """
    if state == DiffieHellmanState.INITIALIZING:
        return "encryptionToken" in request.payload
    elif state == DiffieHellmanState.EXCHANGING_KEYS:
        return "publicKey" in request.payload and "encryptionToken" in request.payload


def authenticated(handler: Callable[[Data], Response]):
    """
    Decorator function to authenticate incoming requests.

    Args:
    - handler (Callable[[Data], Response]): The handler function to be wrapped.

    Returns:
    - Callable[[Data], Response]: The wrapped handler function.
    """

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
