from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from lingua_loop.api.routers import transcript
from lingua_loop.constants import STATIC_DIR
from lingua_loop.constants import TEMPLATES_DIR
from lingua_loop.db.session import create_db_and_tables
from lingua_loop.db.session import get_engine_and_session_maker
from lingua_loop.db.session import shutdown
from lingua_loop.exceptions import TranscriptNotFoundError


def create_app() -> FastAPI:
    async_engine, async_session_maker = get_engine_and_session_maker()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await create_db_and_tables(async_engine=async_engine)
        yield
        await shutdown(async_engine=async_engine)

    app = FastAPI(lifespan=lifespan)

    @app.exception_handler(TranscriptNotFoundError)
    async def transcript_not_found_handler(
        request: Request, exc: TranscriptNotFoundError
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(Path(f"{TEMPLATES_DIR}/index.html"))

    app.include_router(transcript.router)

    return app


app = create_app()
