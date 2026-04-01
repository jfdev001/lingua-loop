from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.transcript import read_or_create_transcript
from lingua_loop.db.transcript import read_segments_by_video_and_ixs
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


async def compute_score(
    video_id: str, segment_ixs: list[int], user_text: str, session: AsyncSession
):
    # TODO: get the language from the segmenst??? could add language field...
    segments_by_ixs = await read_segments_by_video_and_ixs(
        video_id=video_id, segment_ixs=segment_ixs, session=session
    )
    # TODO: the normalization should use the language as well...
    language = None  # TODO:
    text_normalizer = text_normalizer_factory.create(language=language)
    normalized_user_text = text_normalizer.normalize(text=user_text)
    segments_text = " ".join(
        [segment.text for segment in segments_by_ixs]
    )  # TODO: is this accessible...
    normalized_segments_text = text_normalizer.normalize(text=user_text)
    score = score_text(reference_text=segments_text, user_text=user_text)
    return score
