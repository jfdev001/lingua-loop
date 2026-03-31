from os import environ

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.config import SupportedLanguages
from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.transcript import load
from lingua_loop.db.transcript import score
from tests.config import ENV_DATABASE_PATH
from tests.config import IN_MEMORY


@pytest_asyncio.fixture(scope="module")
async def unit_db_session():
    environ[ENV_DATABASE_PATH] = IN_MEMORY
    from lingua_loop.db import session

    await session.create_db_and_tables()

    async with session.async_session_maker() as db_session:
        yield db_session

    await session.shutdown()


@pytest_asyncio.fixture(scope="module")
async def seeded_db(unit_db_session: AsyncSession):

    transcript = Transcript(
        video_id="tageschau",
        language=SupportedLanguages.ENGLISH,  # adjust if needed
        transcript_type=Transcript.TranscriptType.official,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="hello world"),
        Segment(start=2.0, duration=2.0, text="this is a test"),
        Segment(start=4.0, duration=2.0, text="goodbye"),
    ]

    transcript.segments.extend(segments)

    unit_db_session.add(transcript)

    await unit_db_session.commit()
    return unit_db_session


@pytest.mark.asyncio
async def test_seed_test_data(seeded_db: AsyncSession):
    result = await seeded_db.execute(select(Transcript))
    videos = result.scalars().all()
    assert len(videos) == 1


@pytest.mark.asyncio
async def test_load(seeded_db: AsyncSession):
    video_id = "something"  # TODO: place holder
    load(video_id=video_id)  # TODO: this probably needs the db session right??


@pytest.mark.asyncio
async def test_score(seeded_db: AsyncSession):
    # TODO: place holder data...
    segment_ids = [1, 2, 3]
    user_text = "something"
    video_id = "something"
    score(
        video_id=video_id, segment_ids=segment_ids, user_text=user_text
    )  # TODO: probably needs db session???
