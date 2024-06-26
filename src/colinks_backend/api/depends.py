from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from colinks_backend.db.engine import get_db_session

db_session = Annotated[AsyncSession, Depends(get_db_session)]
