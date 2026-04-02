from os import environ

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.constants import ENV_DATABASE_PATH
from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.transcript import read_or_create_transcript
from lingua_loop.db.transcript import read_transcript_with_segments
from lingua_loop.integrations.youtube.types import SupportedLanguages
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
async def test_read_or_create_transcript_in_db(seeded_db: AsyncSession):
    german = SupportedLanguages.GERMAN
    transcript = await read_or_create_transcript(
        video_id=TEST_VIDEO_ID, language=german, session=seeded_db
    )
    assert transcript and transcript.video_id == TEST_VIDEO_ID


@pytest.mark.asyncio
@pytest.mark.slow
async def test_read_or_create_transcript_not_in_db(seeded_db: AsyncSession):
    german = SupportedLanguages.GERMAN
    tagesschau_20260330 = "KKC8HRkTzAY"
    n_segments_tagesschau_20260330 = 249
    transcript = await read_or_create_transcript(
        video_id=tagesschau_20260330, language=german, session=seeded_db
    )
    assert transcript and (
        transcript.video_id == tagesschau_20260330
        and n_segments_tagesschau_20260330
        and transcript.transcript_type == Transcript.TranscriptType.official
    )


@pytest.mark.asyncio
async def test_read_transcript_with_segments(seeded_db: AsyncSession):
    transcript = await read_transcript_with_segments(
        video_id=TEST_VIDEO_ID,
        session=seeded_db,
    )
    segments = transcript.segments
    assert segments and len(segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT
