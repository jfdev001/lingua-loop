from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from lingua_loop.config import SupportedLanguages


class Base(DeclarativeBase):
    pass


class Video(Base):
    __tablename__ = "video"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]

    transcripts = relationship(back_populates="video")


class Transcript(Base):
    __tablename__ = "transcript"
    __table_args__ = UniqueConstraint(
        "video_id",
        "language",
        "transcript_type",
        name="uq_transcript_per_video_language_transcript_type",
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    language: Mapped[SupportedLanguages] = mapped_column(
        SqlEnum(SupportedLanguages)
    )

    class TranscriptType(str, Enum):
        official = "official"
        auto = "auto"

    transcript_type: Mapped[TranscriptType] = mapped_column(
        SqlEnum(TranscriptType)
    )

    created_at = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    video_id = mapped_column(ForeignKey("video.id"))
    video = relationship(back_populates="transcripts")
    segments: Mapped[List["Segment"]] = relationship(
        back_populates="transcript",
        cascade="all, delete-orphan",
        order_by="Segment.start",
    )


class Segment(Base):
    __tablename__ = "segment"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start: Mapped[float]
    duration: Mapped[float]
    text: Mapped[str]

    transcript_id = mapped_column(ForeignKey("transcript.id"))
    transcript: Mapped[Transcript] = relationship(back_populates="segments")
