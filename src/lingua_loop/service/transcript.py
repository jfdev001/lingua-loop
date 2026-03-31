"""CRUD operations do not have Depends(...)... and they are called BY the API

NOTE: This file does also technically contain service logic... but this
is acceptable given how small the app is at this point.

E.g.,

# @file crud/weathers.py
# https://github.com/ArjanCodes/examples/blob/b681c00b038a890d36faa6340a1885b7a6ea5433/2024/tuesday_tips/fastapi_custom_exceptions/skypulse/app/crud/weathers.py#L10
async def get_weather(db_session: AsyncSession, weather_id: int) -> Weather:
    weather = (
        await db_session.scalars(
            select(models.Weather).where(models.Weather.id == weather_id)
        )
    ).first()
    if not weather:
        raise EntityDoesNotExistError
    return weather

# @file api/weathers.py
# https://github.com/ArjanCodes/examples/blob/main/2024/tuesday_tips/fastapi_custom_exceptions/skypulse/app/api/routes/weathers.py
@router.get("/weather/{weather_id}", response_model=Weather)
async def get_weather(
    weather_id: int, db: AsyncSession = Depends(get_db_session)
) -> Weather:
    logger.info(f"Fetching weather with id: {weather_id}")
    weather = await weathers.get_weather(db, weather_id)
    logger.info(f"Fetched weather: {weather}")
    return weather
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.models import Transcript
from lingua_loop.db.models import Video
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import VideoRead


async def fetch_transcript(video_id) -> dict:
    return {}


async def load_video(video_id: str, session: AsyncSession):
    """
    Load video from DB. If not present, fetch transcript and store it.
    """

    # -------------------------
    # check DB
    # -------------------------

    query = select(Video).where(Video.id == video_id)
    # TODO: this belongs in the DB section, not in the service section...
    result = await session.execute(query)
    video: Video | None = result.scalar_one_or_none()
    return video  # TODO: fix this
    if video:
        return video

    # -------------------------
    # fetch transcript externally
    # -------------------------

    transcript_data = await fetch_transcript(video_id)

    # -------------------------
    # create DB objects
    # -------------------------

    video = Video(id=video_id, title=transcript_data["title"])

    transcript = Transcript(
        video=video,
        language=transcript_data["language"],
        type=Transcript.Type(transcript_data["type"]),
    )

    segments = [
        Segment(
            start=s["start"],
            duration=s["duration"],
            text=s["text"],
        )
        for s in transcript_data["segments"]
    ]

    transcript.segments = segments

    session.add(video)

    await session.commit()
    await session.refresh(video)

    # -------------------------
    # return schema
    # -------------------------

    return video


async def compute_score(
    request: ScoreRequest, session: AsyncSession
) -> ScoreResponse:
    return ScoreResponse(score=0.0, expected_text="crud expected")
