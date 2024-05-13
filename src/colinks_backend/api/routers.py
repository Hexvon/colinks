import requests
from fastapi import APIRouter, HTTPException, Body, Path
from sqlalchemy import select, insert
from starlette.responses import RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from colinks_backend.api.depends import db_session
from colinks_backend.api.models import Link, SourceLink
from colinks_backend.api.ops import generate_random_str
from colinks_backend.db import Links

router = APIRouter(
    prefix="/api/links",
    tags=["links"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=Link)
async def create_short_link(
    db: db_session,
    link: SourceLink = Body(),
):
    if requests.head(link.source_link).status_code != 200:
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "Not a valid URL or the URL does not exist.")

    while True:
        gen_str = generate_random_str()
        if not (await db.execute(select(Links).where(Links.short_link == gen_str))).one_or_none():
            await db.execute(insert(Links).values(short_link=gen_str, source_link=link.source_link))
            await db.commit()
            return Link(source_link=link.source_link, short_link=gen_str)


@router.get("/{short_link}", response_model=None)
async def get_source_link(
    db: db_session,
    short_link: str = Path(max_length=7),
):
    url = (await db.scalars(select(Links).where(Links.short_link == short_link))).one_or_none()
    if url is None:
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "Not a valid short URL or the URL does not exist.")

    return RedirectResponse(url=url.source_link)
