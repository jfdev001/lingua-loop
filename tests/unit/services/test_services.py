"""Structural tests (i.e., with mocking of internals) for services layer."""

from math import isclose
from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from lingua_loop.constants import MAX_SCORE
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.services.text_normalization import text_normalizer_factory
from lingua_loop.services.transcript import _score_text
from lingua_loop.services.transcript import compute_score
from lingua_loop.services.transcript import (
    get_or_create_transcript_with_segments,
)

SERVICES = "lingua_loop.services.transcript"


@pytest.mark.asyncio
async def test_get_or_create_transcript(mocker: MockerFixture):
    # Mock db internals for `get_transcript`
    mock_db_result = mocker.Mock()
    video_id = "abc123"
    mock_db_result.video_id = video_id
    language_code = SupportedLanguageCodes.ENGLISH

    mock_db_result.language_code = language_code

    mock_read_or_create_transcript = mocker.patch(
        f"{SERVICES}.read_or_create_transcript_with_segments",
        new_callable=AsyncMock,
    )
    mock_read_or_create_transcript.return_value = mock_db_result

    mock_session = mocker.Mock()

    # Call with mocked internals
    mock_transcript = await get_or_create_transcript_with_segments(
        video_id=video_id,
        language_code=language_code,
        session=mock_session,
    )
    assert mock_transcript

    # Check internal calls
    mock_read_or_create_transcript.assert_awaited_once_with(
        video_id=video_id,
        language_code=language_code,
        session=mock_session,
    )

    # Check mocked output
    assert mock_transcript.video_id == video_id
    assert mock_transcript.language_code == language_code


SCORE_TEXT_TEST_CASES = (
    ["i hate sand", "i hate sand", 1.00],
    ["erklaerung", "erklarung", 0.947],
    ["nailed it", "not really", 0.111],
)


@pytest.mark.parametrize(
    "reference_text,user_text,reference_score", SCORE_TEXT_TEST_CASES
)
def test_score_text(
    reference_text: str, user_text: str, reference_score: float
):
    computed_score = _score_text(
        reference_text=reference_text, user_text=user_text
    )
    assert isclose(computed_score, reference_score, rel_tol=1e-3)


NORMALIZE_TEST_CASES = (
    ["Dat was een ruïne", SupportedLanguageCodes.DUTCH, "dat was een ruine"],
    ["I hate sand.", SupportedLanguageCodes.ENGLISH, "i hate sand"],
    [
        "Er hat gesagt, daß Döner schöner macht. Eine übliche Erklärung.",
        SupportedLanguageCodes.GERMAN,
        "er hat gesagt dass doener schoener macht eine uebliche erklaerung",
    ],
    ["Lui è interesante", SupportedLanguageCodes.ITALIAN, "lui è interesante"],
)


@pytest.mark.parametrize("text,language,normalized_text", NORMALIZE_TEST_CASES)
def test_text_normalizer(text, language, normalized_text):
    text_normalizer = text_normalizer_factory(language_code=language)
    assert text_normalizer.normalize(text=text) == normalized_text


@pytest.mark.asyncio
async def test_compute_score(mocker: MockerFixture):
    """TODO: seems to rely a lot on internal details..."""
    # define mocked internal functions
    mock_read_or_create_transcript_with_segments = mocker.patch(
        f"{SERVICES}.read_or_create_transcript_with_segments"
    )
    mock_transcript = mocker.Mock()
    mock_transcript.language_code = SupportedLanguageCodes.ENGLISH
    mock_read_or_create_transcript_with_segments.return_value = mock_transcript

    mock_get_transcript_segments_by_indices = mocker.patch(
        f"{SERVICES}._get_transcript_segments_by_indices"
    )
    mock_segments_by_indices = mocker.Mock()
    mock_segment_1 = mocker.Mock()
    mock_segment_1.text = "Hello"
    mock_segment_2 = mocker.Mock()
    mock_segment_2.text = "world"
    mock_segments_by_indices = [mock_segment_1, mock_segment_2]
    mock_get_transcript_segments_by_indices.return_value = (
        mock_segments_by_indices
    )

    # test the function of interest
    video_id = "abc123"
    language_code = SupportedLanguageCodes.ENGLISH
    segment_indices = [0, 1]
    user_text = " ".join(list(map(lambda s: s.text, mock_segments_by_indices)))
    mock_session = mocker.Mock()
    mock_score, _ = await compute_score(
        video_id=video_id,
        segment_indices=segment_indices,
        user_text=user_text,
        session=mock_session,
        language_code=language_code,
    )

    assert mock_score == MAX_SCORE

    # assert calls to mocked functions
    mock_read_or_create_transcript_with_segments.assert_awaited_once_with(
        video_id=video_id, session=mock_session, language_code=language_code
    )

    mock_get_transcript_segments_by_indices.assert_called_once_with(
        transcript=mock_transcript, segment_indices=segment_indices
    )
