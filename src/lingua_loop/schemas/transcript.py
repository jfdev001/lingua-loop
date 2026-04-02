from typing import List

from pydantic import BaseModel
from pydantic import Field

from lingua_loop.constants import MAX_SCORE
from lingua_loop.constants import MIN_SCORE


class Segment(BaseModel):
    id: int = Field(ge=0)
    start: float = Field(ge=0.0)
    duration: float = Field(gt=0.0)
    text: str = Field(min_length=1)


class TranscriptResponse(BaseModel):
    video_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    segments: List[Segment]


class ScoreRequest(BaseModel):
    video_id: str = Field(min_length=1)
    segment_indices: List[int] = Field(min_length=1)
    user_text: str = Field(min_length=1)


class ScoreResponse(BaseModel):
    score: float = Field(ge=MIN_SCORE, le=MAX_SCORE)
    reference_text: str = Field(min_length=1)
