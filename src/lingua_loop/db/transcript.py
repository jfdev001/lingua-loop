from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from youtube_transcript_api import FetchedTranscript

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.integrations.youtube.wrapper import fetch_transcript
from lingua_loop.integrations.youtube.wrapper import find_transcript
from lingua_loop.integrations.youtube.wrapper import list_transcripts


def get_segments(fetched_transcript: FetchedTranscript) -> List[Segment]:
    raise NotImplementedError


def normalize(segments: list[Segment]) -> List[Segment]:
    raise NotImplemented


async def cache_transcript(
    video_id: str, language: SupportedLanguages, session: AsyncSession
) -> Transcript | None:
    transcript: Transcript | None = None
    transcript_list = list_transcripts(video_id=video_id)
    transcript_meta = find_transcript(
        transcript_list=transcript_list, language=language
    )
    if transcript_meta:
        fetched_transcript = fetch_transcript(
            video_id=video_id, language=language
        )
        transcript_type = (
            Transcript.TranscriptType.generated
            if fetched_transcript.is_generated
            else Transcript.TranscriptType.official
        )
        transcript = Transcript(
            video_id=video_id,
            language=language,
            transcript_type=transcript_type,
        )

        segments = get_segments(fetched_transcript=fetched_transcript)
        normalized_segments = normalize(segments=segments)
        transcript.segments.extend(normalized_segments)

        session.add(transcript)
        await session.commit()

    return transcript


async def load(
    video_id: str, language: SupportedLanguages, session: AsyncSession
) -> Transcript | None:
    result = await session.execute(
        select(Transcript).where(Transcript.video_id == video_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        transcript = await cache_transcript(
            video_id=video_id, language=language, session=session
        )
    return transcript


async def score(
    video_id: str, segment_ids: list[int], session: AsyncSession
) -> list[Segment] | None:
    raise NotImplementedError
