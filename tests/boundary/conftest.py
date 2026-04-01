import pytest
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.integrations.youtube.wrapper import list_transcripts
from tests.constants import TAGESSCHAU_VID_OFFICIAL


@pytest.fixture(scope="session")
def ytt_api():
    return YouTubeTranscriptApi()


@pytest.fixture(scope="session")
def german_transcript(ytt_api: YouTubeTranscriptApi):
    tagesschau_transcript = ytt_api.fetch(
        TAGESSCHAU_VID_OFFICIAL, languages=[SupportedLanguages.GERMAN]
    )
    return tagesschau_transcript


@pytest.fixture(scope="session")
def transcript_list():
    return list_transcripts(video_id=TAGESSCHAU_VID_OFFICIAL)
