from typing import List

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
    segments: List[Segment]


class ScoreRequest(BaseModel):
    video_id: str
    segment_ixs: List[int] = Field(min_length=1)
    user_text: str = Field(min_length=1)


class ScoreResponse(BaseModel):
    score: float
    segments: List[Segment]
