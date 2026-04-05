from math import isclose
from os import remove

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.constants import MAX_SCORE
from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.session import create_db_and_tables
from lingua_loop.db.session import get_async_session
from lingua_loop.db.session import get_engine_and_session_maker
from lingua_loop.db.session import shutdown
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.main import app
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import TranscriptResponse
from tests.conftest import MockYoutube
from tests.constants import INTEGRATION_ENGLISH_VIDEO_ID
from tests.constants import INTEGRATION_GERMAN_VIDEO_ID
from tests.constants import N_SEGMENTS_IN_TEST_TRANSCRIPT
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
        is_generated=False,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="hello world"),
        Segment(start=2.0, duration=2.0, text="this is a test"),
        Segment(start=4.0, duration=2.0, text="goodbye"),
    ]

    assert len(segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT

    transcript.segments.extend(segments)

    my_db_session.add(transcript)

    await my_db_session.commit()
    return my_db_session


async def seed_dummy_german_transcript(my_db_session: AsyncSession):
    transcript = Transcript(
        video_id=INTEGRATION_GERMAN_VIDEO_ID,
        language_code=SupportedLanguageCodes.GERMAN,
        is_generated=False,
    )

    segments = [
        Segment(start=0.0, duration=2.0, text="Döner macht schöner."),
        Segment(start=2.0, duration=2.0, text="Ein üblicher Ausdruck."),
        Segment(start=4.0, duration=2.0, text="Wie heißen die Männer?"),
    ]

    assert len(segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT

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
    """Per test application

    NOTE: By overriding the get_async_session dependency, I fail to test that
    aspect of the application. In end to end testing, any issues at that
    related to that would only arise during end-to-end testing...
    """

    async def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    yield app
    app.dependency_overrides.pop(get_async_session)


@pytest_asyncio.fixture
async def client(app_with_db: FastAPI):
    """Per test HTTP client that requests the ASGI app(lication)"""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_db), base_url="http://test"
    ) as _client:
        yield _client


@pytest.mark.asyncio
async def test_seed_test_data(seeded_db_session: AsyncSession):
    result = await seeded_db_session.execute(select(Transcript))
    transcripts = result.scalars().all()
    assert len(transcripts) == 2


GET_TRANSCRIPT_TEST_CASES = (
    [INTEGRATION_ENGLISH_VIDEO_ID, SupportedLanguageCodes.ENGLISH, True],
    [INTEGRATION_GERMAN_VIDEO_ID, SupportedLanguageCodes.GERMAN, True],
    ["dummy_vid_not_in_db", SupportedLanguageCodes.DUTCH, False],
)


@pytest.mark.parametrize(
    "video_id,language_code,in_db", GET_TRANSCRIPT_TEST_CASES
)
@pytest.mark.asyncio
async def test_get_transcript_integration(
    video_id: str,
    language_code: SupportedLanguageCodes,
    in_db: bool,
    client: AsyncClient,
    mock_youtube: MockYoutube,
):
    response = await client.get(
        f"/api/transcript/{video_id}/{language_code.value}"
    )

    assert response.status_code == status.HTTP_200_OK

    parsed = TranscriptResponse.model_validate_json(response.content)
    assert parsed.video_id == video_id
    assert len(parsed.segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT

    if not in_db:
        mock_youtube.fetch_transcript.assert_called_once()
        mock_youtube.list_transcripts.assert_called_once()
        mock_youtube.video_has_transcript_in_language.assert_called_once()


SCORE_TRANSCRIPTION_TEST_CASES = (
    [
        INTEGRATION_ENGLISH_VIDEO_ID,
        SupportedLanguageCodes.ENGLISH,
        "hello world this is a test goodbye",
        "hello world this is a test goodbye",
        MAX_SCORE,
    ],
    [
        INTEGRATION_GERMAN_VIDEO_ID,
        SupportedLanguageCodes.GERMAN,
        "Döner schöner.",
        "Döner macht schöner. Ein üblicher Ausdruck. Wie heißen die Männer?",
        0.1307,
    ],
)


@pytest.mark.parametrize(
    "video_id,language_code,user_text,reference_text,expected_score",
    SCORE_TRANSCRIPTION_TEST_CASES,
)
@pytest.mark.asyncio
async def test_score_transcription_integration(
    video_id: str,
    language_code: SupportedLanguageCodes,
    user_text: str,
    reference_text: str,
    expected_score: float,
    client: AsyncClient,
    mock_youtube: MockYoutube,
):
    payload = ScoreRequest(
        video_id=video_id,
        language_code=language_code,
        segment_indices=[0, 1, 2],
        user_text=user_text,
    ).model_dump()

    response = await client.post("/api/score", json=payload)

    assert response.status_code == status.HTTP_200_OK

    parsed = ScoreResponse.model_validate_json(response.content)
    assert isclose(parsed.score, expected_score, rel_tol=1e-3)
    assert parsed.reference_text == reference_text
