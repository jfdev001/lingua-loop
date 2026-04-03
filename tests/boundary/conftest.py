from random import randint
from random import random
from time import sleep

import pytest
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.integrations.youtube.wrapper import list_transcripts
from tests.constants import TAGESSCHAU_VIDEO_ID


def delay():
    sleep(random() * randint(1, 5))


@pytest.fixture(scope="session")
def ytt_api():
    return YouTubeTranscriptApi()


@pytest.fixture(scope="session")
def german_transcript(ytt_api: YouTubeTranscriptApi):
    delay()
    tagesschau_transcript = ytt_api.fetch(
        TAGESSCHAU_VIDEO_ID, languages=[SupportedLanguageCodes.GERMAN]
    )
    return tagesschau_transcript


@pytest.fixture(scope="session")
def transcript_list():
    delay()
    return list_transcripts(video_id=TAGESSCHAU_VIDEO_ID)
