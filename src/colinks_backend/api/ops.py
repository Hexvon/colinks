from uuid6 import uuid7


def generate_random_str():
    return str(uuid7())[:7]
