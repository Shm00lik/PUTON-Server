import json
import random

def is_json(value) -> bool:
    """
    Checks if a string represents valid JSON data.

    Args:
    - value: The string to be checked.

    Returns:
    - bool: True if the string represents valid JSON data, False otherwise.
    """
    try:
        json.loads(value)
    except ValueError:
        return False

    return True

def generate_salt(length: int = 16) -> str:
    """
    Generates a random salt for encryptions

    Returns:
    - str: Generated salt
    """
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(ALPHABET) for i in range(length))