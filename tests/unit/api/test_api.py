from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient
from pytest_mock import MockerFixture

from lingua_loop.db.session import get_async_session
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.main import app as lingua_loop_app
from lingua_loop.schemas.transcript import TranscriptResponse

API = "lingua_loop.api.routers.transcript"


@pytest_asyncio.fixture
async def app(mocker: MockerFixture) -> AsyncGenerator[FastAPI]:
    async def override_get_async_session():
        yield mocker.AsyncMock()

    lingua_loop_app.dependency_overrides[get_async_session] = (
        override_get_async_session
    )
    yield lingua_loop_app
    lingua_loop_app.dependency_overrides.pop(get_async_session)


@pytest_asyncio.fixture
async def client(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as _client:
        yield _client


@pytest.mark.asyncio
async def test_get_transcript_success(
    client: AsyncClient, mocker: MockerFixture
):
    # mock internals
    mock_get_or_create_transcript_with_segments = mocker.patch(
        f"{API}.get_or_create_transcript_with_segments",
    )
    mock_transcript = mocker.Mock()
    mock_segment = mocker.Mock()
    mock_segment.start = 0.0
    mock_segment.duration = 4.2
    mock_segment.text = "slow hello"
    mock_transcript.segments = [mock_segment]
    mock_get_or_create_transcript_with_segments.return_value = mock_transcript

    # test endpoint
    video_id = "abc123"
    language_code = SupportedLanguageCodes.ENGLISH.value
    url = f"/api/transcript/{video_id}/{language_code}"

    response = await client.get(url=url)
    assert response.status_code == status.HTTP_200_OK

    parsed = TranscriptResponse.model_validate_json(response.content)
    assert parsed.video_id == video_id
    assert len(parsed.segments) == len(mock_transcript.segments)

    # assert call to mocked function
    mock_get_or_create_transcript_with_segments.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_transcript_invalid_video_id(client, mocker: MockerFixture):
    raise


@pytest.mark.asyncio
async def test_score_transcription_success(client, mocker: MockerFixture):
    raise


@pytest.mark.asyncio
async def test_score_transcription_invalid_segment_ixs(
    client, mocker: MockerFixture
):
    raise
