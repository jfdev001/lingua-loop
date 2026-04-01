import pytest
from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import TranscriptList

from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.integrations.youtube.wrapper import fetch_transcript
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
    german = SupportedLanguages.GERMAN
    transcript = fetch_transcript(
        video_id=TAGESSCHAU_VID_OFFICIAL, language=german
    )
    assert transcript.snippets is not None


@pytest.mark.slow
def test_find_transcript(transcript_list: TranscriptList):
    german = SupportedLanguages.GERMAN
    transcript = find_transcript(
        transcript_list=transcript_list, language=german
    )
    assert transcript and transcript.language_code == german
