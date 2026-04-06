from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient
from pytest_mock import MockerFixture

from lingua_loop.db.session import get_async_session
from lingua_loop.exceptions import SegmentIndicesError
from lingua_loop.exceptions import TranscriptNotFoundError
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.main import app as lingua_loop_app
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
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
    mock_transcript.is_generated = False
    mock_get_or_create_transcript_with_segments.return_value = mock_transcript

    # request endpoint
    video_id = "abc123"
    language_code = SupportedLanguageCodes.ENGLISH.value
    url = f"/api/transcript/{video_id}/{language_code}"
    response = await client.get(url=url)

    # check response
    assert response.status_code == status.HTTP_200_OK
    parsed = TranscriptResponse.model_validate_json(response.content)
    assert parsed.video_id == video_id
    assert len(parsed.segments) == len(mock_transcript.segments)

    # check mocked internals
    mock_get_or_create_transcript_with_segments.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_transcript_invalid_video_id(
    client: AsyncClient, mocker: MockerFixture
):
    # mock internals
    video_id = "invalid_id"
    mock_get_or_create_transcript_with_segments = mocker.patch(
        f"{API}.get_or_create_transcript_with_segments",
        new=mocker.AsyncMock(
            side_effect=TranscriptNotFoundError(video_id=video_id)
        ),
    )

    # request endpoint
    language_code = SupportedLanguageCodes.ENGLISH.value
    url = f"/api/transcript/{video_id}/{language_code}"
    response = await client.get(url=url)

    # check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    detail = response.json()["detail"]
    assert detail == f"Transcript not found for video_id={video_id}"


@pytest.mark.asyncio
async def test_score_transcription_success(
    client: AsyncClient, mocker: MockerFixture
):
    # mock internals
    mock_validate_score_request = mocker.patch(
        f"{API}._validate_score_request", new=mocker.AsyncMock()
    )

    mock_compute_score = mocker.patch(f"{API}.compute_score")
    mock_score = 0.625  # expected result of _score_text(...)
    mock_reference_text = "Hello world!"
    mock_compute_score.return_value = (mock_score, mock_reference_text)

    # request endpoint
    video_id = "abc123"
    language_code = SupportedLanguageCodes.ENGLISH
    segment_indices = [0]
    user_text = "The world!"
    payload = ScoreRequest(
        language_code=language_code,
        segment_indices=segment_indices,
        user_text=user_text,
        video_id=video_id,
    ).model_dump()

    url = "/api/score"
    response = await client.post(url=url, json=payload)

    # check response
    assert response.status_code == status.HTTP_200_OK
    parsed = ScoreResponse.model_validate_json(response.content)
    assert parsed.score == mock_score
    assert parsed.reference_text == mock_reference_text

    # check mocked internals
    mock_validate_score_request.assert_awaited_once()
    mock_compute_score.assert_awaited_once()


@pytest.mark.asyncio
async def test_score_transcription_invalid_segment_ixs(
    client: AsyncClient, mocker: MockerFixture
):
    # mock internals
    invalid_segment_indices = [999]
    mock_validate_score_request = mocker.patch(
        f"{API}._validate_score_request",
        new=mocker.AsyncMock(
            side_effect=SegmentIndicesError(
                segment_indices=invalid_segment_indices
            )
        ),
    )

    # request endpoint
    video_id = "abc123"
    language_code = SupportedLanguageCodes.ENGLISH
    user_text = "a transcription attempt"
    payload = ScoreRequest(
        video_id=video_id,
        language_code=language_code,
        segment_indices=invalid_segment_indices,
        user_text=user_text,
    ).model_dump()

    url = "/api/score"
    response = await client.post(url=url, json=payload)

    # check response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
