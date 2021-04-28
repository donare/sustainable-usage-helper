from sqlalchemy import String, Integer, Time
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.config import Base, LIMIT
from app.db.schemas import TimeFrameCreate
from app.db.models.base import BaseMixin
from fastapi import HTTPException, status


class TimeFrame(Base, BaseMixin):
    start_time = Column(Time, index=True)
    end_time = Column(Time, index=True)
    weekdays = Column(Integer, index=True)

    block_set_id = Column(Integer, ForeignKey("blockset.id"))
    block_set = relationship("BlockSet", back_populates="timeframe", lazy='selectin')

    def __init__(self, time_frame: TimeFrameCreate):
        self.start_time = time_frame.start_time
        self.end_time = time_frame.end_time
        self.weekdays = time_frame.weekdays
