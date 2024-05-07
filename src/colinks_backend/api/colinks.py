from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from colinks_backend.db.engine import get_db_session

router = APIRouter(
    prefix="/api/links",
    tags=["links"],
    responses={404: {"description": "Not found"}},
)

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
