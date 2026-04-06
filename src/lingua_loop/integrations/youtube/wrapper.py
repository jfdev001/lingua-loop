from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import NoTranscriptFound
from youtube_transcript_api import TranscriptList
from youtube_transcript_api import YouTubeTranscriptApi

from lingua_loop.integrations.youtube.types import SupportedLanguageCodes

ytt_api = YouTubeTranscriptApi()


def fetch_transcript(
    video_id: str, language_code: SupportedLanguageCodes
) -> FetchedTranscript:
    return ytt_api.fetch(video_id=video_id, languages=[language_code])


def list_transcripts(video_id: str) -> TranscriptList:
    return ytt_api.list(video_id)


def video_has_transcript_in_language(
    transcript_list: TranscriptList, language_code: SupportedLanguageCodes
) -> bool:
    transcript_found = True
    try:
        transcript = transcript_list.find_transcript(
            language_codes=[language_code]
        )
    except NoTranscriptFound:
        transcript_found = False
    return transcript_found
