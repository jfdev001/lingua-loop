from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

from lingua_loop.config import SupportedLanguages

ytt_api = YouTubeTranscriptApi()

tagesschau_vid_official = "_RoFnUnT060"

tagesschau_transcripts = ytt_api.fetch(tagesschau_vid_official,
                                       languages=[SupportedLanguages.GERMAN])

ez_dutch_vid_automatic = "Lkjo9UR03wQ"

ez_dutch_transcripts = ytt_api.fetch(ez_dutch_vid_automatic,
                                     languages=[SupportedLanguages.DUTCH])

print("end")
