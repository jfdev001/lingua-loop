"""Structural tests (i.e., with mocking of internals) for services layer."""

from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.services.text_normalization import text_normalizer_factory
from lingua_loop.services.transcript import compute_score
from lingua_loop.services.transcript import get_transcript


@pytest.mark.asyncio
async def test_get_transcript(mocker: MockerFixture):
    # Mock db internals for `get_transcript`
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

    # Call with mocked internals
    mock_transcript = await get_transcript(
        video_id=video_id,
        language=language,
        session=mock_session,
    )
    assert mock_transcript

    # Check internal calls
    mock_read_or_create_transcript.assert_awaited_once_with(
        video_id=video_id,
        language=language,
        session=mock_session,
    )

    # Check mocked output
    assert mock_transcript.video_id == video_id
    assert mock_transcript.language == language


def test_score_text():
    raise NotImplementedError


NORMALIZE_TEST_CASES = (
    [
        "Er hat gesagt, daß Döner schöner macht. Eine übliche Erklärung.",
        SupportedLanguages.GERMAN,
        "Er hat gesagt, dass Doener schoener macht. Eine uebliche Erklaerung.",
    ],
    ["I hate sand.", SupportedLanguages.ENGLISH, "I hate sand."],
)


@pytest.mark.parametrize("text,language,normalized_text", NORMALIZE_TEST_CASES)
def test_text_normalizer(text, language, normalized_text):
    text_normalizer = text_normalizer_factory(language=language)
    assert text_normalizer.normalize(text=text) == normalized_text


@pytest.mark.asyncio
async def test_compute_score(mocker: MockerFixture):
    """TODO: seems to rely a lot on internal details..."""
    # define mocked internal functions
    mock_read_transcript_with_segments = mocker.patch(
        "lingua_loop.services.transcript.read_transcript_with_segments"
    )
    mock_transcript = mocker.Mock()
    mock_transcript.language = SupportedLanguages.ENGLISH
    mock_read_transcript_with_segments.return_value = mock_transcript

    mock_get_transcript_segments_by_ixs = mocker.patch(
        "lingua_loop.services.transcript.get_transcript_segments_by_ixs"
    )
    mock_segments_by_ixs = mocker.Mock()
    mock_segment_1 = mocker.Mock()
    mock_segment_1.text = "Hello"
    mock_segment_2 = mocker.Mock()
    mock_segment_2.text = "world"
    mock_segments_by_ixs = [mock_segment_1, mock_segment_2]
    mock_get_transcript_segments_by_ixs.return_value = mock_segments_by_ixs

    # test the function of interest
    video_id = "abc123"
    segment_ixs = [0, 1]
    user_text = " ".join(list(map(lambda s: s.text, mock_segments_by_ixs)))
    mock_session = mocker.Mock()
    mock_score = await compute_score(
        video_id=video_id,
        segment_ixs=segment_ixs,
        user_text=user_text,
        session=mock_session,
    )

    # assert calls to mocked functions
    mock_read_transcript_with_segments.assert_awaited_once_with(
        video_id=video_id, session=mock_session
    )

    mock_get_transcript_segments_by_ixs.assert_called_once_with(
        transcript=mock_transcript, segment_ixs=segment_ixs
    )

    perfect_score = 1.0
    assert mock_score == perfect_score
