from sqlalchemy.orm import Mapped, mapped_column

from colinks_backend.db.base import Base


class Links(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(index=True, unique=True)
    short_link: Mapped[str] = mapped_column(index=True, unique=True)
