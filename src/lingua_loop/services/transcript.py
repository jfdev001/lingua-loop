from difflib import SequenceMatcher
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
    """
    TODO: At some point, you may want to give the user information about
    word level mismatches so that they can see roughly what they missed...
    the current approach just gives an overall score. It also performs
    no weighting, so each word is worth as much as the previous...
    """
    ref_words = reference_text.split()
    user_words = user_text.split()

    max_n_words = max(len(ref_words), len(user_words))
    max_score = 1.0
    if max_n_words == 0:  # handles no inputs
        return max_score

    # zip truncates lists... therefore missing/extra words implicitly penalized
    # via division by max_n_words
    total = 0.0
    elements_in_str_to_ignore = None
    for ref_word, user_word in zip(ref_words, user_words):
        ratio = SequenceMatcher(
            elements_in_str_to_ignore, ref_word, user_word
        ).ratio()
        total += ratio

    return total / max_n_words


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
    assert is_monotonically_increasing(segment_ixs)
    segments = transcript.segments
    segments = [segments[ix] for ix in segment_ixs]
    return segments


async def compute_score(
    video_id: str, segment_ixs: list[int], user_text: str, session: AsyncSession
) -> float:

    transcript = await read_transcript_with_segments(
        video_id=video_id, session=session
    )

    language = transcript.language
    text_normalizer = text_normalizer_factory(language=language)

    segments_by_ixs = get_transcript_segments_by_ixs(
        transcript=transcript, segment_ixs=segment_ixs
    )
    segments_text = " ".join([segment.text for segment in segments_by_ixs])

    normalized_segments_text = text_normalizer.normalize(text=segments_text)
    normalized_user_text = text_normalizer.normalize(text=user_text)

    score = score_text(
        reference_text=normalized_segments_text, user_text=normalized_user_text
    )

    return score
