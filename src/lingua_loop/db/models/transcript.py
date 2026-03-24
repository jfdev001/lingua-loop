# NOTE: forecast-in-a-box puts database models (i.e., Column etc.) into
# the schemas... is this a reasonable approach??... yes but really Field should
# go into API related stuff since schemas defines what API acceps and returns..
# not necessarily what the Database (directly) receives...
# Comparatively... netflix/dispatch just has a single dir for some logic
# and puts models.py in defining both database models and schemas (API)
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True)
    title = Column(String)
    transcript = relationship(
        "Transcript", back_populates="video", uselist=False)


class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String, ForeignKey("videos.id"), unique=True)
    language = Column(String)

    class Type(str, Enum):
        official = "official"
        auto = "auto"
    type = Column(SqlEnum(Type))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    video = relationship("Video", back_populates="transcript")
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
