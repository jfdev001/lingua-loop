from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.db.models import Segment
from lingua_loop.db.session import get_async_session
from lingua_loop.exceptions import SegmentIndicesError
from lingua_loop.integrations.youtube.types import SupportedLanguageCodes
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import SegmentSchema
from lingua_loop.schemas.transcript import TranscriptResponse
from lingua_loop.services.transcript import compute_score
from lingua_loop.services.transcript import (
    get_or_create_transcript_with_segments,
)

router = APIRouter()


@router.get(
    "/api/transcript/{video_id}/{language_code}",
    response_model=TranscriptResponse,
)
async def get_transcript(
    video_id: str,
    language_code: SupportedLanguageCodes,
    session=Depends(get_async_session),
):
    transcript = await get_or_create_transcript_with_segments(
        video_id=video_id, language_code=language_code, session=session
    )

    segments = _segments_to_schema(segments=transcript.segments)

    transcript_response = TranscriptResponse(
        video_id=video_id, segments=segments
    )
    return transcript_response


def _segments_to_schema(segments: List[Segment]) -> List[SegmentSchema]:
    segments_as_schema = [
        SegmentSchema(
            start=segment.start, duration=segment.duration, text=segment.text
        )
        for segment in segments
    ]
    return segments_as_schema


@router.post("/api/score", response_model=ScoreResponse)
async def score_transcription(
    request: ScoreRequest,
    session: AsyncSession = Depends(get_async_session),
):
    await _validate_score_request(request=request, session=session)

    # Score the request
    score, reference_text = await compute_score(
        video_id=request.video_id,
        segment_indices=request.segment_indices,
        user_text=request.user_text,
        language_code=request.language_code,
        session=session,
    )
    score_response = ScoreResponse(score=score, reference_text=reference_text)
    return score_response


async def _validate_score_request(
    request: ScoreRequest, session: AsyncSession
) -> None:
    transcript = await get_or_create_transcript_with_segments(
        video_id=request.video_id,
        session=session,
        language_code=request.language_code,
    )

    segments = transcript.segments
    if any(i < 0 or i >= len(segments) for i in request.segment_indices):
        raise SegmentIndicesError(segment_indices=request.segment_indices)

    return
