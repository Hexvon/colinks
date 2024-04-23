from typing import List
from typing import Optional

import sqlalchemy
from sqlalchemy import Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from colinks_backend.config import CONFIG


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String)
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="addresses")


engine = sqlalchemy.create_engine(CONFIG.DATABASE_URL)
meta = MetaData()


def create_all():
    with engine.connect() as conn:
        with conn.begin():
            meta.create_all(conn)
        meta.reflect(conn)

