from os import environ
from os import remove
from os.path import exists

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.constants import ENV_DATABASE_PATH
from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.integrations.youtube.types import SupportedLanguages
from tests.constants import TEST_DATABASE_PATH


@pytest_asyncio.fixture(scope="module")
async def integration_db_session():
    """NOTE: just in case manual integration tests are needed..."""
    environ[ENV_DATABASE_PATH] = TEST_DATABASE_PATH

    if exists(TEST_DATABASE_PATH):
        remove(TEST_DATABASE_PATH)

    from lingua_loop.db import session

    await session.create_db_and_tables()

    async with session.async_session_maker() as db_session:
        yield db_session

    await session.shutdown()


@pytest_asyncio.fixture(scope="module")
async def seeded_db(integration_db_session: AsyncSession):
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

    integration_db_session.add(transcript)

    await integration_db_session.commit()
    return integration_db_session


@pytest.mark.asyncio
async def test_seed_test_data(seeded_db: AsyncSession):
    result = await seeded_db.execute(select(Transcript))
    videos = result.scalars().all()
    assert len(videos) == 1


def test_integration():
    """TODO: should use schemathesis and hypothesis"""
    raise NotImplementedError
