"""CRUD operations do not have Depends(...)... and they are called BY the API

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
from lingua_loop.schemas.transcript import ScoreRequest, ScoreResponse, VideoRead
from sqlalchemy.ext.asyncio import AsyncSession


async def load_video(video_id: str, session: AsyncSession) -> VideoRead:
    return VideoRead(id="crud video", title="crud title")


async def compute_score(request: ScoreRequest, session: AsyncSession) -> ScoreResponse:
    return ScoreResponse(score=0.0, expected_text="crud expected")
