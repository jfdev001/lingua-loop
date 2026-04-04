from contextlib import asynccontextmanager
from typing import Dict
from typing import List
from typing import TypedDict

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from lingua_loop.api.routers import transcript
from lingua_loop.constants import STATIC_DIR
from lingua_loop.constants import TEMPLATES_DIR
from lingua_loop.db.session import create_db_and_tables
from lingua_loop.db.session import get_engine_and_session_maker
from lingua_loop.db.session import shutdown
from lingua_loop.exceptions import TranscriptNotFoundError
from lingua_loop.integrations.youtube.types import language_code_to_language


class State(TypedDict):
    async_session_maker: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(app: FastAPI):
    async_engine, async_session_maker = get_engine_and_session_maker()
    await create_db_and_tables(async_engine=async_engine)
    yield {"async_session_maker": async_session_maker}
    await shutdown(async_engine=async_engine)


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    @app.exception_handler(TranscriptNotFoundError)
    async def transcript_not_found_handler(
        request: Request, exc: TranscriptNotFoundError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    templates = Jinja2Templates(directory=TEMPLATES_DIR)

    @app.get("/", include_in_schema=False)
    def index(request: Request):
        # NOTE: maybe just do regular dict instead of list of dicts??
        languages: List[Dict] = [
            {"language_code": language_code.value, "language": language.value}
            for language_code, language in language_code_to_language.items()
        ]
        return templates.TemplateResponse(
            request, "index.html", {"languages": languages}
        )

    app.include_router(transcript.router)

    return app


app = create_app()
