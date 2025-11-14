from __future__ import annotations

import pathlib
from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

DB_PATH = pathlib.Path(__file__).resolve().parent.parent / "sentinel.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(ENGINE)


@contextmanager
def get_session() -> Iterator[Session]:
    with Session(ENGINE, expire_on_commit=False) as session:
        yield session

