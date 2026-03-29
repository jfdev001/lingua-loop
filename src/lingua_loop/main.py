from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from lingua_loop.api.routers import transcript
from lingua_loop.config import STATIC_DIR, TEMPLATES_DIR
from lingua_loop.db import session
from lingua_loop.models.transcript import ScoreRequest, ScoreResponse, VideoRead


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
