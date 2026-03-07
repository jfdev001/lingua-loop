from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from lingua_loop.config import STATIC_DIR, TEMPLATES_DIR
from lingua_loop.db import session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await session.create_db_and_tables()
    yield
    await session.shutdown()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TODO: This is API (i.e., what the backend acceptsand returns)
# stuff and should live in another directory... see
# e.g., forecast-in-a-box
# pydantic base models needed here also...
# TODO: put also Field here


@app.get("/api/videos/load")
def load_video():
    pass


@app.get("/api/transcripts/load")
def load_transcripts():
    """Don't do this until the user wants to score..."""
    #
    pass


@app.get("/api/transcripts/segment")
def segment_transcripts():
    """ """
    pass


@app.post("/api/score")
def score():
    """on submit then a score can be output"""
    pass
