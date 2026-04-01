from typing import Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript


async def load(video_id: str, session: AsyncSession) -> Transcript | None:
    result = await session.execute(
        select(Transcript).where(Transcript.video_id == video_id)
    )
    transcript = result.scalar_one_or_none()
    if not transcript:
        raise NotImplementedError
    return transcript


async def score(
    video_id: str, segment_ids: list[int], user_text: str, session: AsyncSession
) -> Tuple[float, str, list[Segment]]:
    """TODO: returning Tuple seems bad practice, maybe use Pydantic schema alr here???"""
    raise NotImplementedError
