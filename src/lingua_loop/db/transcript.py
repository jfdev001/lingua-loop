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
        # TODO: get primary langauge from transcript..
        # list transcript
        # find transcript to see if it has language code
        # fetched_transcript = fetch_transcript(video_id=video_id)
        raise
    return transcript


async def score(
    video_id: str, segment_ids: list[int], session: AsyncSession
) -> list[Segment] | None:
    raise NotImplementedError
