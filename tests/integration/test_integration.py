from os import remove

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.session import create_db_and_tables
from lingua_loop.db.session import get_async_session
from lingua_loop.db.session import get_engine_and_session_maker
from lingua_loop.db.session import shutdown
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.main import app
from tests.constants import INTEGRATION_ENGLISH_VIDEO_ID
from tests.constants import INTEGRATION_GERMAN_VIDEO_ID
from tests.constants import TEST_DATABASE_PATH


@pytest_asyncio.fixture(scope="module")
async def db_session():
    """Single global db session with db as file"""
    async_engine, async_session_maker = get_engine_and_session_maker(
        database_path=TEST_DATABASE_PATH
    )
    await create_db_and_tables(async_engine=async_engine)

    async with async_session_maker() as _db_session:
        yield _db_session

    await shutdown(async_engine=async_engine)
    remove(TEST_DATABASE_PATH)


async def seed_dummy_english_transcript(my_db_session: AsyncSession):
    transcript = Transcript(
        video_id=INTEGRATION_ENGLISH_VIDEO_ID,
        language_code=SupportedLanguageCodes.ENGLISH,
        transcript_type=Transcript.TranscriptType.official,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="hello world"),
        Segment(start=2.0, duration=2.0, text="this is a test"),
        Segment(start=4.0, duration=2.0, text="goodbye"),
    ]

    transcript.segments.extend(segments)

    my_db_session.add(transcript)

    await my_db_session.commit()
    return my_db_session


async def seed_dummy_german_transcript(my_db_session: AsyncSession):
    transcript = Transcript(
        video_id=INTEGRATION_GERMAN_VIDEO_ID,
        language_code=SupportedLanguageCodes.GERMAN,
        transcript_type=Transcript.TranscriptType.official,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="Döner macht schöner."),
        Segment(start=2.0, duration=2.0, text="Ein üblicher Ausdruck."),
        Segment(start=4.0, duration=2.0, text="Wie heißen die Männer?"),
    ]

    transcript.segments.extend(segments)

    my_db_session.add(transcript)

    await my_db_session.commit()
    return my_db_session


@pytest_asyncio.fixture(scope="module")
async def seeded_db_session(db_session: AsyncSession):
    """Single global db with dummy data."""
    db_session = await seed_dummy_english_transcript(db_session)
    db_session = await seed_dummy_german_transcript(db_session)
    return db_session


@pytest_asyncio.fixture
async def app_with_db(db_session: AsyncSession):
    """Per test application"""

    async def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    yield app

    app.dependency_overrides.pop(get_async_session)


@pytest_asyncio.fixture
async def client(app_with_db: FastAPI):
    """Per test client"""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_db), base_url="http://test"
    ) as _client:
        yield _client


@pytest.mark.asyncio
async def test_seed_test_data(seeded_db_session: AsyncSession):
    result = await seeded_db_session.execute(select(Transcript))
    transcripts = result.scalars().all()
    assert len(transcripts) == 2


def test_integration(client: AsyncClient):
    raise NotImplementedError
