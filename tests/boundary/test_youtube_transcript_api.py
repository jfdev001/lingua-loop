import pytest
from youtube_transcript_api import FetchedTranscript

from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.integrations.youtube.wrapper import fetch_transcript
from tests.constants import TAGESSCHAU_VID_OFFICIAL


@pytest.mark.slow
def test_transcript(transcript: FetchedTranscript):
    snippets = transcript.snippets
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
