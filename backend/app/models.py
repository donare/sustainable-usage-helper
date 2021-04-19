from sqlalchemy import String, Integer, Time
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


# association_table = Table(
#     "association",
#     Base.metadata,
#     Column("left_id", Integer, ForeignKey("left.id")),
#     Column("right_id", Integer, ForeignKey("right.id"))
# )


class Application(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    app_path = Column(String, unique=True, index=True)

    block_sets = relationship("BlockSet", back_populates="apps")


class BlockSet(Base):
    __tablename__ = "block_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    applications = relationship("Application", back_populates="block_sets")
    time_frames = relationship("TimeFrame", back_populates="block_sets")


class TimeFrame(Base):
    __tablename__ = "time_frames"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time, index=True)
    end_time = Column(Time, index=True)
    weekdays = Column(Integer, index=True)

    block_sets = relationship("BlockSet", back_populates="time_frames")
