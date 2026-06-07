"""Database session management utilities."""

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Tuple

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from lingua_loop.constants import DEFAULT_DATABASE_PATH
from lingua_loop.constants import DEFAULT_DB_DRIVER
from lingua_loop.db.models import Base


def get_engine_and_session_maker(
    db_driver: str = DEFAULT_DB_DRIVER,
    database_path: Path | str = DEFAULT_DATABASE_PATH,
) -> Tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Create and return the async engine and session maker."""
    sqlalchemy_database_url = f"{db_driver}:///{database_path}"
    async_engine = create_async_engine(sqlalchemy_database_url)
    async_session_maker = async_sessionmaker(
        async_engine, expire_on_commit=False
    )
    return async_engine, async_session_maker


async def create_db_and_tables(async_engine: AsyncEngine):
    """Create all database tables defined in models."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown(async_engine: AsyncEngine):
    """Dispose of the async engine."""
    await async_engine.dispose()


async def get_async_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    """Provide an async database session for dependency injection."""

    # `state` property of `request` gets populated by main.py::lifespan
    async_session_maker = request.state.async_session_maker

    async with async_session_maker() as session:
        yield session
