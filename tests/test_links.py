import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from colinks_backend.utils.http_client import json_or_raise


@pytest.mark.asyncio
async def test_colinks_endpoints(db_session: AsyncSession, create_test_async_client: AsyncClient):
    client = create_test_async_client

    source_link = "https://example.com/"
    create_rsp = json_or_raise(await client.post("api/links/create", json={"source_link": source_link}))

    assert create_rsp["source_link"] == source_link

    short_link = create_rsp["short_link"]
    get_rsp = json_or_raise(await client.get(f"api/links/{short_link}"))

    assert get_rsp["source_link"] == source_link
