from pydantic import BaseModel
from pydantic import Field


class Segment(BaseModel):
    id: int
    start: float
    duration: float
    text: str


class TranscriptResponse(BaseModel):
    video_id: str
    title: str
    segments: list[Segment]


class ScoreRequest(BaseModel):
    video_id: str
    segment_ids: list[int] = Field(min_length=1)
    user_text: str = Field(min_length=1)


class ScoreResponse(BaseModel):
    score: float
    segments: list[Segment]
