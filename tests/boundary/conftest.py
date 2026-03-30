import pytest
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.config import SupportedLanguages


@pytest.fixture(scope="session")
def ytt_api():
    return YouTubeTranscriptApi()


@pytest.fixture(scope="session")
def transcript(ytt_api: YouTubeTranscriptApi):
    tagesschau_vid_official = "_RoFnUnT060"
    tagesschau_transcripts = ytt_api.fetch(
        tagesschau_vid_official, languages=[SupportedLanguages.GERMAN]
    )
    return tagesschau_transcripts
