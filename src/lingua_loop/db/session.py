from collections.abc import AsyncGenerator
from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from lingua_loop.config import DEFAULT_ENV_DATABASE_PATH
from lingua_loop.config import DEFAULT_ENV_DB_DRIVER
from lingua_loop.config import ENV_DATABASE_PATH
from lingua_loop.config import ENV_DB_DRIVER
from lingua_loop.db.models import Base

DATABASE_PATH = getenv(ENV_DATABASE_PATH, DEFAULT_ENV_DATABASE_PATH)
DB_DRIVER = getenv(ENV_DB_DRIVER, DEFAULT_ENV_DB_DRIVER)

# TODO: this should be function to prevent module scope (causes issues
# only in test env...)
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
