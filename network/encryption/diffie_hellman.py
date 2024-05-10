from enum import Enum
import random


class DiffieHellman:
    """
    A class implementing the Diffie-Hellman key exchange protocol.
    """

    P = 9_007_199_254_740_881  # A large prime number
    G = 2  # Generator

    @staticmethod
    def generate_public_key(private_key: int) -> int:
        """
        Generates a public key based on the provided private key.

        Args:
        - private_key (int): The private key.

        Returns:
        - int: The public key.
        """
        # G^private_key % P
        return pow(DiffieHellman.G, private_key, DiffieHellman.P)

    @staticmethod
    def generate_shared_key(other_public_key: int, private_key: int) -> int:
        """
        Generates a shared key based on the provided other party's public key and own private key.

        Args:
        - other_public_key (int): The other party's public key.
        - private_key (int): Own private key.

        Returns:
        - int: The shared key.
        """
        # other_public_key^private_key % P
        return pow(other_public_key, private_key, DiffieHellman.P)

    @staticmethod
    def generate_private_key(min: int = 10, max: int = 20) -> int:
        """
        Generates a random private key within a specific range.

        Returns:
        - int: The generated private key.
        """
        return random.randint(min, max)

    @staticmethod
    def get_public_params() -> dict[str, int]:
        """
        Returns public parameters (G and P) used in the Diffie-Hellman key exchange.

        Returns:
        - dict[str, int]: A dictionary containing 'g' (generator) and 'p' (prime modulus).
        """
        return {"g": DiffieHellman.G, "p": DiffieHellman.P}


class DiffieHellmanState(Enum):
    """
    Enumeration representing states of the Diffie-Hellman key exchange.
    """

    INITIALIZING = 1
    EXCHANGING_KEYS = 3
