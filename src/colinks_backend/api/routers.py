import logging

import httpx
from fastapi import APIRouter, HTTPException, Body, Path
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND

from colinks_backend.api.depends import db_session
from colinks_backend.api.models import Link, SourceLink
from colinks_backend.api.ops import generate_random_str
from colinks_backend.config import CONFIG
from colinks_backend.db import Links

router = APIRouter(
    prefix="/links",
    tags=["Links"],
)

logger = logging.getLogger()


@router.post("/create", response_model=Link)
async def create_short_link(
    db: db_session,
    link: SourceLink = Body(),
):
    async with httpx.AsyncClient() as client:
        link_response = await client.get(link.source_link, timeout=10)
        logger.debug(link_response)
        if link_response.status_code != 200:
            raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "Not a valid URL or the URL does not exist.")

    while True:
        gen_str = generate_random_str()
        try:
            db.add(Links(short_link=gen_str, source_link=link.source_link))
            await db.commit()
            break
        except IntegrityError as e:
            pass
        except Exception as e:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, e)
    return Link(source_link=link.source_link, short_link=CONFIG.host + gen_str)


@router.get("/{short_link}", response_model=None)
async def get_source_link(
    db: db_session,
    short_link: str = Path(),
):
    url = (await db.scalars(select(Links).where(Links.short_link == short_link))).one_or_none()
    if url is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not a valid short link or the link does not exist.")

    return SourceLink(source_link=url.source_link)
