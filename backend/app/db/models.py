from sqlalchemy import String, Integer, Time
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.db.config import Base


block_associations = Table(
    "block_set_associations",
    Base.metadata,
    Column("apps_id", Integer, ForeignKey("apps.id")),
    Column("block_sets_id", Integer, ForeignKey("block_sets.id"))
)


class Application(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    app_path = Column(String, unique=True, index=True)

    block_sets = relationship("BlockSet", secondary=block_associations, back_populates="apps")


class BlockSet(Base):
    __tablename__ = "block_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    apps = relationship("Application", secondary=block_associations, back_populates="block_sets")
    time_frames = relationship("TimeFrame", back_populates="block_set")


class TimeFrame(Base):
    __tablename__ = "time_frames"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time, index=True)
    end_time = Column(Time, index=True)
    weekdays = Column(Integer, index=True)

    block_set_id = Column(Integer, ForeignKey("block_sets.id"))
    block_set = relationship("BlockSet", back_populates="time_frames")