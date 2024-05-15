from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from colinks_backend.utils.http_client import json_or_raise


async def test_my_crud_function(db_session: AsyncSession, create_test_async_client: AsyncClient, session_override):
    client = create_test_async_client

    source_link = "https://example.com/"
    rsp = json_or_raise(await client.post("api/links/create", json={"source_link": source_link}))

    assert rsp["source_link"] == source_link
