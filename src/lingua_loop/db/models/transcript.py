# TODO: this is where you should put Column info... i.e., what the database
# tables look like and the relationship between the tables ...
# see /home/jf01/dev/FastAPIPhotoVideoSharing/app/db.py
# NOTE: forecast-in-a-box puts database description (i.e., Column etc.) into
# the schemas... is this a reasonable approach??... yes but really Field should
# go into API related stuff since schemas defines what API acceps and returns..
# not necessarily what the Database (directly) receives
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship


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
