from sqlalchemy.ext.asyncio import AsyncSession


def load(video_id: str, session: AsyncSession):
    raise NotImplementedError


def score(
    video_id: str, segment_ids: list[int], user_text: str, session: AsyncSession
):
    raise NotImplementedError
