from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import AsyncSession

from lingua_loop.config import STATIC_DIR, TEMPLATES_DIR
from lingua_loop.db import session
from lingua_loop.schemas.transcript import ScoreRequest, ScoreResponse, VideoRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    await session.create_db_and_tables()
    yield
    await session.shutdown()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(Path(f"{TEMPLATES_DIR}/index.html"))

# TODO: This is API (i.e., what the backend accepts and returns)
# stuff and should live in another directory... see
# e.g., forecast-in-a-box uses app.include_router to handle api end points
# https://fastapi.tiangolo.com/reference/apirouter/


@app.get("/api/video/load/{video_id}", response_model=VideoRead)
def load_video(
        video_id: str,
        session: AsyncSession = Depends(session.get_async_session)):
    """"""
    return VideoRead(id=video_id, title="dummy title")


# @app.get("/api/transcript/load")
# def load_transcripts(
#         video_id: str,
#         session: AsyncSession = Depends(session.get_async_session)):
#     """Don't do this until the user wants to score..."""
#     #
#     pass
#
#
# @app.get("/api/transcript/segment")
# def segment_transcripts(
#         video_id: str,
#         session: AsyncSession = Depends(session.get_async_session)):
#     """ """
#     pass


@app.post("/api/score", response_model=ScoreResponse)
def score(request: ScoreRequest):
    """on submit then a score can be output

    Should query the transcript at this point since user doesn't need it 
    unless they wish to transcribe...

    Should also send the start time information of the youtube video?? or 
    should limit start times only to those corresponding to segments in the 
    actually transcripts... to do that... the load_video DOES need to have
    transcripts available to it to 
    """
    # TODO: use the video id and segment id to get the corresponding
    # segment of the transcript from the database with the exact text...
    # note that it could be a list of segment ids!!
    return ScoreResponse(score=0.0, expected_text="expected transcription")
