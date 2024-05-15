from fastapi import Path, HTTPException, APIRouter
from sqlalchemy import select
from starlette.responses import RedirectResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from colinks_backend.api.depends import db_session
from colinks_backend.db import Links

router = APIRouter(
    prefix="",
    tags=["Redirect"],
)


@router.get("/{short_link}", response_model=None)
async def get_source_link(
    db: db_session,
    short_link: str = Path(max_length=7),
):
    url = (await db.scalars(select(Links).where(Links.short_link == short_link))).one_or_none()
    if url is None:
        raise HTTPException(HTTP_422_UNPROCESSABLE_ENTITY, "Not a valid short link or the link does not exist.")

    return RedirectResponse(url=url.source_link)
