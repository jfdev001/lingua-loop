from typing import List

from pydantic import BaseModel
from pydantic import Field

from lingua_loop.constants import MAX_SCORE
from lingua_loop.constants import MIN_SCORE
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes


class SegmentSchema(BaseModel):
    start: float = Field(ge=0.0)
    duration: float = Field(gt=0.0)
    text: str = Field(min_length=1)


class TranscriptResponse(BaseModel):
    video_id: str = Field(min_length=1)
    segments: List[SegmentSchema]


class ScoreRequest(BaseModel):
    video_id: str = Field(min_length=1)
    segment_indices: List[int] = Field(min_length=1)
    user_text: str = Field(min_length=1)
    language_code: SupportedLanguageCodes


class ScoreResponse(BaseModel):
    score: float = Field(ge=MIN_SCORE, le=MAX_SCORE)
    reference_text: str = Field(min_length=1)
