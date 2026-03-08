# NOTE: Forecast in a box puts Field declaration (i.e., for the API response)
# in their schemas (e.g.,
# https://github.com/ecmwf/forecast-in-a-box/blob/2240e30852ba008cdf91c1a5a2f4dd092c96678c/backend/src/forecastbox/schemas/user.py#L16-L25)
# but also they put database models into schemas
# https://github.com/ecmwf/forecast-in-a-box/blob/2240e30852ba008cdf91c1a5a2f4dd092c96678c/backend/src/forecastbox/schemas/schedule.py#L21-L32
# NOTE: arjan code examples show also how it's common to have a base
# and then define different response types for each CRUD operation
# https://github.com/ArjanCodes/examples/blob/b681c00b038a890d36faa6340a1885b7a6ea5433/2024/tuesday_tips/fastapi_custom_exceptions/skypulse/app/schemas/city.py
# and could also split up any CRUD application logic into a separate folder
# if needed... whatever... don't worry about this for now...

# In either case... the typical approach is to put Field stuff into schemas dir:w
# NAMING should be CRUD based
from pydantic import BaseModel, ConfigDict


class BaseReadModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SegmentRead(BaseReadModel):
    start: float
    duration: float
    text: str


class TranscriptRead(BaseReadModel):
    id: int
    type: str
    language: str
    segments: list[SegmentRead]


class VideoRead(BaseReadModel):
    id: str
    title: str
    transcripts: list[TranscriptRead] = []
