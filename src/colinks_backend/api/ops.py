import base64
import secrets


def generate_random_str():
    return base64.b64encode(secrets.token_bytes(6), altchars=b"_-").decode()
