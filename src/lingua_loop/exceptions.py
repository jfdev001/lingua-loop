"""Custom exceptions for Lingua Loop."""

from fastapi import status
from fastapi.exceptions import HTTPException


class TranscriptNotFoundError(Exception):
    """Raised when a transcript is not found for a given video ID."""

    def __init__(self, video_id: str):
        """Initialize the exception with the video_id."""
        self.video_id = video_id
        super().__init__(f"Transcript not found for video_id={video_id}")


class SegmentIndicesError(HTTPException):
    """Raised when invalid segment indices are provided."""

    def __init__(self, segment_indices: list[int]):
        """Initialize the exception with the invalid segment_indices."""
        status_code = status.HTTP_400_BAD_REQUEST
        detail = f"Invalid segment indices, got {segment_indices}"
        super().__init__(status_code=status_code, detail=detail)
