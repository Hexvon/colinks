import httpx
from fastapi import APIRouter, HTTPException, Body
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from colinks_backend.api.depends import db_session
from colinks_backend.api.models import Link, SourceLink
from colinks_backend.api.ops import generate_random_str
from colinks_backend.db import Links

router = APIRouter(
    prefix="/api/links",
    tags=["Links"],
)


@router.post("/create", response_model=Link)
async def create_short_link(
    db: db_session,
    link: SourceLink = Body(),
):
    async with httpx.AsyncClient() as client:
        if (await client.get(link.source_link, timeout=10)).status_code != 200:
            raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "Not a valid URL or the URL does not exist.")

    while True:
        gen_str = generate_random_str()
        try:
            db.add(Links(short_link=gen_str, source_link=link.source_link))
            await db.commit()
            break
        except Exception as e:
            pass
    return Link(source_link=link.source_link, short_link=gen_str)