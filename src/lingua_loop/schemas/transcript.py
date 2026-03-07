# TODO: check out schemas here /home/jf01/dev/FastAPIPhotoVideoSharing/app/db.py
# Note though that it seems Field should go in an api/ folder (per also
# forecast-in-a-box???
from pydantic import BaseModel


class SegmentSchema(BaseModel):
    start: float
    duration: float
    text: str

    class Config:
        orm_mode = True


class TranscriptSchema(BaseModel):
    id: int
    type: str
    language: str
    segments: list[SegmentSchema]

    class Config:
        orm_mode = True


class VideoSchema(BaseModel):
    id: str
    title: str
    transcripts: list[TranscriptSchema] = []

    class Config:
        orm_mode = True
