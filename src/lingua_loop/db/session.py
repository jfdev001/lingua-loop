from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from lingua_loop.schemas import transcript

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./transcripts.db"
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown():
    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
