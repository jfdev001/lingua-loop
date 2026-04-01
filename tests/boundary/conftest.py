import pytest
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.integrations.youtube.types import SupportedLanguages
from tests.constants import TAGESSCHAU_VID_OFFICIAL


@pytest.fixture(scope="session")
def ytt_api():
    return YouTubeTranscriptApi()


@pytest.fixture(scope="session")
def transcript(ytt_api: YouTubeTranscriptApi):
    tagesschau_transcripts = ytt_api.fetch(
        TAGESSCHAU_VID_OFFICIAL, languages=[SupportedLanguages.GERMAN]
    )
    return tagesschau_transcripts
