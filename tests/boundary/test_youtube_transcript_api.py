import pytest
from youtube_transcript_api import FetchedTranscript


@pytest.mark.slow
def test_transcript(transcript: FetchedTranscript):
    snippets = transcript.snippets
    assert isinstance(snippets, list)

    snippet = snippets[0]
    assert isinstance(snippet.duration, float)
    assert isinstance(snippet.start, float)
    assert isinstance(snippet.text, str)
