from youtube_transcript_api import FetchedTranscript
import pytest


@pytest.mark.slow
def test_transcript(transcript: FetchedTranscript):
    # snippets = transcript.snippets
    # for snippet in snippets:
    #     print()
    assert False
