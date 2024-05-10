import json


def is_json(value):
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
