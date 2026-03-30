from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from lingua_loop.api.routers import transcript
from lingua_loop.config import STATIC_DIR
from lingua_loop.config import TEMPLATES_DIR
from lingua_loop.db import session
from lingua_loop.schemas.transcript import ScoreRequest
from lingua_loop.schemas.transcript import ScoreResponse
from lingua_loop.schemas.transcript import VideoRead


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


app.include_router(transcript.router)
