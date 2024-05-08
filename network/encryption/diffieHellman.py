from enum import Enum
import random


class DiffieHellman:
    P = 9_007_199_254_740_881
    G = 2

    @staticmethod
    def generate_public_key(private_key: int) -> int:
        # G^private_key mod P
        return pow(DiffieHellman.G, private_key, DiffieHellman.P)

    @staticmethod
    def generate_shared_key(other_public_key: int, private_key: int) -> int:
        # other_public_key^private_key mod P
        return pow(other_public_key, private_key, DiffieHellman.P)

    @staticmethod
    def generate_private_key() -> int:
        return random.randint(10, 20)

    @staticmethod
    def get_public_params() -> dict[str, int]:
        return {"g": DiffieHellman.G, "p": DiffieHellman.P}


class DiffieHellmanState(Enum):
    INITIALIZING = 1
    EXCHANGING_KEYS = 3
