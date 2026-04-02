from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from youtube_transcript_api import FetchedTranscript

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.exceptions import TranscriptNotFoundError
from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.integrations.youtube.wrapper import fetch_transcript
from lingua_loop.integrations.youtube.wrapper import find_transcript
from lingua_loop.integrations.youtube.wrapper import list_transcripts


def _get_segments(fetched_transcript: FetchedTranscript) -> List[Segment]:
    segments: List[Segment] = []
    snippets = fetched_transcript.snippets
    for snippet in snippets:
        start = snippet.start
        duration = snippet.duration
        text = snippet.text
        segment = Segment(start=start, duration=duration, text=text)
        segments.append(segment)
    return segments


async def _create_transcript(
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

        segments = _get_segments(fetched_transcript=fetched_transcript)
        transcript.segments.extend(segments)

        session.add(transcript)
        await session.commit()

    return transcript


async def _read_transcript(
    video_id: str, session: AsyncSession
) -> Transcript | None:
    result = await session.execute(
        select(Transcript).where(Transcript.video_id == video_id)
    )
    transcript = result.scalar_one_or_none()
    return transcript


async def read_or_create_transcript(
    video_id: str, language: SupportedLanguages, session: AsyncSession
) -> Transcript | None:
    transcript = await _read_transcript(video_id=video_id, session=session)
    if not transcript:
        transcript = await _create_transcript(
            video_id=video_id, language=language, session=session
        )
    return transcript


async def read_transcript_with_segments(
    video_id: str, session: AsyncSession
) -> Transcript:
    result = await session.execute(
        select(Transcript)
        .options(selectinload(Transcript.segments))
        .where(Transcript.video_id == video_id)
    )
    transcript = result.scalar_one_or_none()
    if transcript is None:
        raise TranscriptNotFoundError(video_id=video_id)

    return transcript
