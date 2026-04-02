from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from pytest_mock import MockerFixture

from lingua_loop.db.session import get_async_session
from lingua_loop.main import app as lingua_loop_app


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
async def test_get_transcript_success(client, mocker: MockerFixture):
    raise


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
