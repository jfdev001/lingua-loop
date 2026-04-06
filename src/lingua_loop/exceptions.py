from fastapi import status
from fastapi.exceptions import HTTPException


class TranscriptNotFoundError(Exception):
    def __init__(self, video_id: str):
        self.video_id = video_id
        super().__init__(f"Transcript not found for video_id={video_id}")


class SegmentIndicesError(HTTPException):
    def __init__(self, segment_indices: list[int]):
        status_code = status.HTTP_400_BAD_REQUEST
        detail = f"Invalid segment indices, got {segment_indices}"
        super().__init__(status_code=status_code, detail=detail)
