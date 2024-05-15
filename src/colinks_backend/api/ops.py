from uuid import uuid4


def generate_random_str():
    return str(uuid4())[:7]
