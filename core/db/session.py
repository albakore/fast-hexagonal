from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import Session

from core.config.settings import env

session_context: ContextVar[str] = ContextVar("session_context")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


async_engine = create_async_engine(env.DATABASE_URL)
# sync_engine = create_engine(env.ENV)


_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=Session,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)

@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=Session,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()