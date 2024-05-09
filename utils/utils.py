import json


def is_json(value):
    try:
        json.loads(value)
    except ValueError:
        return False

    return True
