from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from lingua_loop.config import DATABASE_PATH
from lingua_loop.config import DB_DRIVER
from lingua_loop.db.models import Base

sqlalchemy_database_url = f"{DB_DRIVER}:///{DATABASE_PATH}"
async_engine = create_async_engine(sqlalchemy_database_url)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown():
    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
