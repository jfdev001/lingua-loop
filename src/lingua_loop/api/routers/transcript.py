from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

import lingua_loop.services.transcript
from lingua_loop.db import session
from lingua_loop.integrations.youtube.types import SupportedLanguages
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import TranscriptResponse

router = APIRouter()


@router.get(
    "/api/transcript/{video_id}/{language_code}",
    response_model=TranscriptResponse,
)
async def get_transcript(
    video_id: str,
    language_code: SupportedLanguages,
    session=Depends(session.get_async_session),
):
    transcript = await lingua_loop.services.transcript.get_or_create_transcript(
        video_id=video_id, language=language_code, session=session
    )

    transcript_response = TranscriptResponse.model_validate(transcript)
    return transcript_response


async def _validate_score_request(
    request: ScoreRequest, session: AsyncSession
) -> None:
    transcript = (
        await lingua_loop.services.transcript.get_transcript_with_segment(
            video_id=request.video_id, session=session
        )
    )

    segments = transcript.segments
    if any(i < 0 or i >= len(segments) for i in request.segment_indices):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid segment index",
        )

    return


@router.post("/api/score", response_model=ScoreResponse)
async def compute_score(
    request: ScoreRequest,
    session: AsyncSession = Depends(session.get_async_session),
):
    # Validate the request
    await _validate_score_request(request=request, session=session)

    # Score the request
    score, reference_text = await lingua_loop.services.transcript.compute_score(
        video_id=request.video_id,
        segment_indices=request.segment_indices,
        user_text=request.user_text,
        session=session,
    )
    score_response = ScoreResponse(score=score, reference_text=reference_text)
    return score_response
