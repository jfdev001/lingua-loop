"""Structural tests (i.e., with mocking of internals) for services layer."""

from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.services.text_normalization import text_normalizer_factory
from lingua_loop.services.transcript import get_transcript


@pytest.mark.asyncio
async def test_get_transcript(mocker: MockerFixture):
    # --- Arrange ---
    mock_db_result = mocker.Mock()
    video_id = "abc123"
    mock_db_result.video_id = video_id
    language = SupportedLanguages.ENGLISH

    mock_db_result.language = language

    mock_read_or_create_transcript = mocker.patch(
        "lingua_loop.services.transcript.read_or_create_transcript",
        new_callable=AsyncMock,
    )
    mock_read_or_create_transcript.return_value = mock_db_result

    mock_session = mocker.Mock()

    # --- Act ---
    mock_transcript = await get_transcript(
        video_id=video_id,
        language=language,
        session=mock_session,
    )

    # --- Assert ---
    mock_read_or_create_transcript.assert_awaited_once_with(
        video_id=video_id,
        language=language,
        session=mock_session,
    )

    assert mock_transcript.video_id == video_id
    assert mock_transcript.language == language


def test_score_text():
    raise NotImplementedError


NORMALIZE_TEST_CASES = (
    [
        "Er hat gesagt, daß Döner schöner macht.",
        SupportedLanguages.GERMAN,
        "Er hat gesagt, dass Doener schoener macht",
    ],
    ["I hate sand", SupportedLanguages.ENGLISH, "I hate sand"],
)


@pytest.mark.parametrize("text,language,normalized_text", NORMALIZE_TEST_CASES)
def test_text_normalizer(text, language, normalized_text):
    text_normalizer = text_normalizer_factory(language=language)
    assert text_normalizer.normalize(text=text) == normalized_text


@pytest.mark.asyncio
async def test_compute_score(mocker: MockerFixture):
    raise NotImplementedError
    # arrange
    # TODO: mock segments (i.e., return of read_segments_by_video_and_ixs)
    # which is an async call
    mock_read_segments_by_video_and_ixs = mocker.patch(
        "lingua_loop.services.transcript.read_segments_by_video_and_ixs"
    )

    video_id = "abc123"
    segment_ixs = [1, 2, 3]

    # TODO: mock args to compute_score
    # video id, session,

    # call
    mock_segments = None

    # assert that the async function occurred once
    mock_read_segments_by_video_and_ixs.assert_awaited_once_with(
        video_id=video_id,
        segment_ixs=segment_ixs,
    )
