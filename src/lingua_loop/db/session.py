from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from lingua_loop.config import DATABASE_PATH
from lingua_loop.db.models.transcript import Base

# TODO: This should be an environment variable probably
# NOTE: will this break due to relative paths and/or OS paths??
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown():
    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
