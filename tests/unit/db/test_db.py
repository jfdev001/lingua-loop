from os import environ

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.config import ENV_DATABASE_PATH
from lingua_loop.config import SupportedLanguages
from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.transcript import load
from lingua_loop.db.transcript import score
from tests.constants import IN_MEMORY
from tests.constants import N_SEGMENTS_IN_TEST_TRANSCRIPT
from tests.constants import TEST_VIDEO_ID


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
        video_id=TEST_VIDEO_ID,
        language=SupportedLanguages.ENGLISH,  # adjust if needed
        transcript_type=Transcript.TranscriptType.official,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="hello world"),
        Segment(start=2.0, duration=2.0, text="this is a test"),
        Segment(start=4.0, duration=2.0, text="goodbye"),
    ]
    assert len(segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT

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
async def test_load_transcript_in_db(seeded_db: AsyncSession):
    load(video_id=TEST_VIDEO_ID, session=seeded_db)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_load_transcript_not_in_db(seeded_db: AsyncSession):
    tagesschau_20260330 = "KKC8HRkTzAY"
    load(video_id=tagesschau_20260330, session=seeded_db)


@pytest.mark.asyncio
async def test_score(seeded_db: AsyncSession):
    segment_ids = list(range(N_SEGMENTS_IN_TEST_TRANSCRIPT))
    user_text = "attempt at transcription here"
    score(
        video_id=TEST_VIDEO_ID,
        segment_ids=segment_ids,
        user_text=user_text,
        session=seeded_db,
    )
