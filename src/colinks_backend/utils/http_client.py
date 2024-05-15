from typing import Any

import httpx


def json_or_raise(resp: httpx.Response) -> Any:
    try:
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise Exception(f"BODY: {resp.json()}") from e
