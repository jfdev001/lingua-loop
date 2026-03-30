from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import lingua_loop.service.transcript
from lingua_loop.db import session
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import VideoRead

router = APIRouter()  # NOTE:  lifespan isn't needed here...


@router.get("/api/video/load/{video_id}", response_model=VideoRead)
async def load_video(
    video_id: str, session: AsyncSession = Depends(session.get_async_session)
):
    """"""
    video = await lingua_loop.service.transcript.load_video(
        video_id=video_id, session=session
    )
    video = VideoRead(id=video_id, title="dummy")  # TODO: filler
    return video


@router.post("/api/score", response_model=ScoreResponse)
async def compute_score(
    request: ScoreRequest,
    session: AsyncSession = Depends(session.get_async_session),
):
    """on submit then a score can be output

    Should also send the start time information of the youtube video?? or
    should limit start times only to those corresponding to segments in the
    actually transcripts... to do that... the load_video DOES need to have
    transcripts available to it to
    """
    # TODO: use the video id and segment id to get the corresponding
    # TODO: depends on video id so needs this from the frontend and it can't
    # be null.... also gets
    # segment of the transcript from the database with the exact text...
    # note that it could be a list of segment ids!!
    score = await crud_transcript.compute_score(
        request=request, session=session
    )
    return score
