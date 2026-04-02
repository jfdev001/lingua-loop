import pytest
from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import TranscriptList

from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.integrations.youtube.wrapper import fetch_transcript
from lingua_loop.integrations.youtube.wrapper import (
    video_has_transcript_in_language,
)
from tests.constants import TAGESSCHAU_VID_OFFICIAL


@pytest.mark.slow
def test_german_transcript(german_transcript: FetchedTranscript):
    snippets = german_transcript.snippets
    assert isinstance(snippets, list)

    snippet = snippets[0]
    assert isinstance(snippet.duration, float)
    assert isinstance(snippet.start, float)
    assert isinstance(snippet.text, str)


@pytest.mark.slow
def test_fetch_transcript():
    german = SupportedLanguageCodes.GERMAN
    transcript = fetch_transcript(
        video_id=TAGESSCHAU_VID_OFFICIAL, language_code=german
    )
    assert transcript.snippets is not None


@pytest.mark.slow
def test_video_had_transcript_in_language(transcript_list: TranscriptList):
    german = SupportedLanguageCodes.GERMAN
    assert video_has_transcript_in_language(
        transcript_list=transcript_list, language_code=german
    )
