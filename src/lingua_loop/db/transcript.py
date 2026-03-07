# TODO: this is where you should put Column info... i.e., what the database
# tables look like and the relationship between the tables ...
# see /home/jf01/dev/FastAPIPhotoVideoSharing/app/db.py
# NOTE: forecast-in-a-box puts database description (i.e.,Field etc.) into
# the schemas... is this a reasonable approach??
from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship

from lingua_loop.schemas import transcript

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./transcripts.db"
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True)
    title = Column(String)

    transcripts = relationship("Transcript", back_populates="video")


class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.id"))
    type = Column(String, default="official")  # official, auto, user
    language = Column(String, default="de")
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="transcripts")
    segments = relationship(
        "Segment", back_populates="transcript", cascade="all, delete-orphan")


class Segment(Base):
    __tablename__ = "segments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transcript_id = Column(Integer, ForeignKey("transcripts.id"))
    start = Column(Float)
    duration = Column(Float)
    text = Column(Text)

    transcript = relationship("Transcript", back_populates="segments")


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(transcript.Base.metadata.create_all)


async def shutdown():
    await async_engine.dispose()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
