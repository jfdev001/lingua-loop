from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.transcript import read_or_create_transcript
from lingua_loop.db.transcript import read_transcript_with_segments
from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.services.text_normalization import text_normalizer_factory


async def get_transcript(
    video_id: str, language: SupportedLanguages, session: AsyncSession
):
    transcript = await read_or_create_transcript(
        video_id=video_id, language=language, session=session
    )
    return transcript


def score_text(reference_text: str, user_text: str):
    raise NotImplementedError


def is_monotonically_increasing(ixs: List[int]) -> bool:
    assert len(ixs) >= 1
    monotonically_increasing: bool = True
    for ix in range(0, len(ixs) - 1):
        cur = ixs[ix]
        next_ = ixs[ix + 1]
        if cur >= next_:
            monotonically_increasing = False
            break
    return monotonically_increasing


def get_transcript_segments_by_ixs(
    transcript: Transcript, segment_ixs: List[int]
) -> List[Segment]:
    segments = transcript.segments
    assert is_monotonically_increasing(segment_ixs)
    segments = [segments[ix] for ix in segment_ixs]
    return segments


async def compute_score(
    video_id: str, segment_ixs: list[int], user_text: str, session: AsyncSession
):

    transcript = await read_transcript_with_segments(
        video_id=video_id, session=session
    )
    segments_by_ixs = get_transcript_segments_by_ixs(
        transcript=transcript, segment_ixs=segment_ixs
    )
    segments_text = " ".join([segment.text for segment in segments_by_ixs])
    language = transcript.language
    text_normalizer = text_normalizer_factory(language=language)
    normalized_segments_text = text_normalizer.normalize(text=segments_text)
    normalized_user_text = text_normalizer.normalize(text=user_text)
    score = score_text(
        reference_text=normalized_segments_text, user_text=normalized_user_text
    )
    return score
