import pytest
import pytest_asyncio
from pytest_mock import MockType
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.session import create_db_and_tables
from lingua_loop.db.session import get_engine_and_session_maker
from lingua_loop.db.session import shutdown
from lingua_loop.db.transcript import read_or_create_transcript_with_segments
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from tests.constants import IN_MEMORY
from tests.constants import N_MOCKED_SEGMENTS
from tests.constants import N_SEGMENTS_IN_TEST_TRANSCRIPT
from tests.constants import TAGESSCHAU_VIDEO_ID
from tests.constants import TEST_VIDEO_ID


@pytest_asyncio.fixture(scope="module")
async def unit_db_session():
    async_engine, async_session_maker = get_engine_and_session_maker(
        database_path=IN_MEMORY
    )
    await create_db_and_tables(async_engine=async_engine)

    async with async_session_maker() as db_session:
        yield db_session

    await shutdown(async_engine=async_engine)


@pytest_asyncio.fixture(scope="module")
async def seeded_db(unit_db_session: AsyncSession):

    transcript = Transcript(
        video_id=TEST_VIDEO_ID,
        language_code=SupportedLanguageCodes.ENGLISH,  # adjust if needed
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
    transcripts = result.scalars().all()
    assert len(transcripts) == 1


@pytest.mark.asyncio
async def test_read_or_create_transcript_in_db(seeded_db: AsyncSession):
    german = SupportedLanguageCodes.GERMAN
    transcript = await read_or_create_transcript_with_segments(
        video_id=TEST_VIDEO_ID, language_code=german, session=seeded_db
    )
    assert transcript.video_id == TEST_VIDEO_ID
    assert len(transcript.segments) == N_SEGMENTS_IN_TEST_TRANSCRIPT


@pytest.mark.asyncio
async def test_read_or_create_transcript_not_in_db(
    seeded_db: AsyncSession,
    mock_fetch_transcript: MockType,
    mock_list_transcripts: MockType,
    mock_video_has_transcript_in_language: MockType,
):
    """
    The mocks here are to avoid hitting the youtube transcript api which occurs
    in `lingua_loop.db.transcript._create_transcript`.
    """
    german = SupportedLanguageCodes.GERMAN
    transcript = await read_or_create_transcript_with_segments(
        video_id=TAGESSCHAU_VIDEO_ID, language_code=german, session=seeded_db
    )

    assert transcript.video_id == TAGESSCHAU_VIDEO_ID
    assert len(transcript.segments) == N_MOCKED_SEGMENTS
    mock_fetch_transcript.assert_called_once()
    mock_list_transcripts.assert_called_once()
    mock_video_has_transcript_in_language.assert_called_once()
