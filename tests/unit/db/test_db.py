from os import environ

import pytest
import pytest_asyncio

from lingua_loop.db.transcript import load
from lingua_loop.db.transcript import score
from tests.config import ENV_DATABASE_PATH
from tests.config import IN_MEMORY


@pytest_asyncio.fixture
async def unit_db_session():
    environ[ENV_DATABASE_PATH] = IN_MEMORY
    from lingua_loop.db import session

    await session.create_db_and_tables()
    # TODO: populate with some dummy data here!!
    # TODO: the dummy args as fixures as well for consitency...
    in_memory_session = session.async_session_maker
    yield in_memory_session
    await session.shutdown()


@pytest.mark.asyncio
async def test_load(unit_db_session):
    video_id = "something"
    load(video_id=video_id)


@pytest.mark.asyncio
async def test_score(unit_db_session):
    segment_ids = [1, 2, 3]
    user_text = "something"
    video_id = "something"
    score(video_id=video_id, segment_ids=segment_ids, user_text=user_text)
