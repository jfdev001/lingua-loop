from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from lingua_loop.config import STATIC_DIR, TEMPLATES_DIR
from lingua_loop.db import transcript


@asynccontextmanager
async def lifespan(app: FastAPI):
    await transcript.create_db_and_tables()
    yield
    await transcript.shutdown()

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


@app.get("/api/transcripts/load")
def load_transcripts():
    #
    pass


@app.get("/api/transcripts/segment")
def segment_transcripts():
    pass


@app.post("/api/score")
def score():
    pass
