"""Youtube transcript api wrapper function mocks"""

import pytest
from pytest_mock import MockerFixture
from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import FetchedTranscriptSnippet

from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.integrations.youtube.types import language_code_to_language
from tests.constants import N_MOCKED_SEGMENTS

# Where the youtube transcript api wrapper functions are imported
DATA_LAYER = "lingua_loop.db.transcript"


@pytest.fixture
def mock_fetch_transcript(mocker: MockerFixture):
    _mock_fetch_transcript = mocker.patch(f"{DATA_LAYER}.fetch_transcript")
    _mock_fetch_transcript.side_effect = fake_fetch_transcript
    return _mock_fetch_transcript


def fake_fetch_transcript(
    video_id: str, language_code: SupportedLanguageCodes
) -> FetchedTranscript:
    snippets = [
        FetchedTranscriptSnippet(
            start=0.0, duration=2.0, text="But what about"
        ),
        FetchedTranscriptSnippet(
            start=2.0, duration=2.0, text="the droid attack"
        ),
        FetchedTranscriptSnippet(
            start=4.0, duration=2.0, text="on the wookies?"
        ),
    ]
    assert len(snippets) == N_MOCKED_SEGMENTS

    transcript = FetchedTranscript(
        video_id=video_id,
        language_code=language_code.value,
        language=language_code_to_language[language_code].value,
        is_generated=False,  # implies official
        snippets=snippets,
    )

    return transcript


@pytest.fixture
def mock_list_transcripts(mocker: MockerFixture):
    """
    Unpopulated mock for TranscriptList since that's only used with
    `youtube/wrapper.py::video_has_transcript_in_language`
    """
    _mock_list_transcripts = mocker.patch(f"{DATA_LAYER}.list_transcripts")
    _mock_list_transcripts.return_value = mocker.Mock()
    return _mock_list_transcripts


@pytest.fixture
def mock_video_has_transcript_in_language(mocker: MockerFixture):
    """
    Mocks that video always has transcript in the desired language, and
    therefore TranscriptNotFoundError in `db/transcript.py::_create_transcript`
    never gets thrown
    """
    _mock_video_has_transcript_in_language = mocker.patch(
        f"{DATA_LAYER}.video_has_transcript_in_language"
    )
    _mock_video_has_transcript_in_language.return_value = True
    return _mock_video_has_transcript_in_language
