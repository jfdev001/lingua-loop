from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from lingua_loop.integrations.youtube.types import SupportedLanguages


class Base(DeclarativeBase):
    pass


class Transcript(Base):
    """One transcript per video for now."""

    __tablename__ = "transcript"
    video_id: Mapped[str] = mapped_column(primary_key=True)
    language: Mapped[SupportedLanguages] = mapped_column(
        SqlEnum(SupportedLanguages)
    )

    class TranscriptType(str, Enum):
        official = "official"
        generated = "generated"

    transcript_type: Mapped[TranscriptType] = mapped_column(
        SqlEnum(TranscriptType)
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

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

    transcript_id: Mapped[str] = mapped_column(
        ForeignKey("transcript.video_id")
    )
    transcript: Mapped[Transcript] = relationship(back_populates="segments")
