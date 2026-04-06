from difflib import SequenceMatcher
from typing import List
from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.transcript import read_or_create_transcript_with_segments
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.services.text_normalization import text_normalizer_factory


async def get_or_create_transcript_with_segments(
    video_id: str,
    language_code: SupportedLanguageCodes,
    session: AsyncSession,
) -> Transcript:
    """Pass through for DB logic for now."""
    transcript = await read_or_create_transcript_with_segments(
        video_id=video_id, language_code=language_code, session=session
    )

    return transcript


async def compute_score(
    video_id: str,
    segment_indices: list[int],
    user_text: str,
    language_code: SupportedLanguageCodes,
    session: AsyncSession,
) -> Tuple[float, str]:

    transcript = await read_or_create_transcript_with_segments(
        video_id=video_id, session=session, language_code=language_code
    )

    text_normalizer = text_normalizer_factory(language_code=language_code)

    segments_by_indices = _get_transcript_segments_by_indices(
        transcript=transcript, segment_indices=segment_indices
    )
    reference_text = " ".join([segment.text for segment in segments_by_indices])

    normalized_reference_text = text_normalizer.normalize(text=reference_text)
    normalized_user_text = text_normalizer.normalize(text=user_text)

    score = _score_text(
        reference_text=normalized_reference_text, user_text=normalized_user_text
    )

    return score, reference_text


def _get_transcript_segments_by_indices(
    transcript: Transcript, segment_indices: List[int]
) -> List[Segment]:
    assert _is_monotonically_increasing(segment_indices)
    segments = transcript.segments
    segments = [segments[ix] for ix in segment_indices]
    return segments


def _is_monotonically_increasing(indices: List[int]) -> bool:
    assert len(indices) >= 1
    monotonically_increasing: bool = True
    for ix in range(0, len(indices) - 1):
        cur = indices[ix]
        next_ = indices[ix + 1]
        if cur >= next_:
            monotonically_increasing = False
            break
    return monotonically_increasing


def _score_text(reference_text: str, user_text: str):
    """
    TODO: At some point, you may want to give the user information about
    word level mismatches so that they can see roughly what they missed...
    the current approach just gives an overall score. It also performs
    no weighting, so each word is worth as much as the previous...
    """
    ref_words = reference_text.split()
    user_words = user_text.split()

    # NOTE: If the user types additional words beyond the reference text,
    # they are not punished
    max_n_words = len(ref_words)

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
