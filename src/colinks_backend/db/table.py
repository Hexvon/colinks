from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped

from colinks_backend.db.base import Base


class Links(Base):
    __tablename__ = "links"

    short_link: Mapped[Annotated[str, mapped_column(primary_key=True, unique=True)]]
    source_link: Mapped[Annotated[str, mapped_column(index=True)]]
    created_at: Mapped[Annotated[datetime, mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP())]]
