from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.integrations.youtube.types import SupportedLanguages

ytt_api = YouTubeTranscriptApi()


def fetch_transcript(
    video_id: str, language: SupportedLanguages
) -> FetchedTranscript:
    return ytt_api.fetch(video_id=video_id, languages=[language])
