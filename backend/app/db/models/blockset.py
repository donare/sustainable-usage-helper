from sqlalchemy import String, Integer, Time
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.config import Base, LIMIT
from app.db.models.associations import block_associations
from app.db.models.base import BaseMixin
from app.db.models.timeframe import TimeFrame
from app.db.models.application import Application
from app.db.schemas import BlockSetCreate
from fastapi import HTTPException, status


class BlockSet(Base, BaseMixin):
    name = Column(String)

    apps = relationship("Application", secondary=block_associations, back_populates="blockset", lazy='selectin')
    time_frames = relationship("TimeFrame", back_populates="block_set", lazy='selectin')

    def __init__(self, block_set: BlockSetCreate):
        self.name = block_set.name
        self.apps = []
        self.time_frames = []

    @classmethod
    async def add_time_frame(cls, db_session: AsyncSession, block_set_id: int, time_frame: TimeFrame):
        block_set = await cls.find_by_id(db_session, block_set_id)
        block_set.time_frames.append(time_frame)
        await db_session.commit()
        await db_session.refresh(block_set)
        return block_set

    @classmethod
    async def get_applications(cls, db_session, block_set_id: int):
        block_set = await cls.find_by_id(db_session, block_set_id)
        return block_set.apps

    @classmethod
    async def block_application(cls, db_session: AsyncSession, block_set_id: int, app: Application):
        block_set = await cls.find_by_id(db_session, block_set_id)
        block_set.apps.append(app)
        await db_session.commit()
        return block_set

    @classmethod
    async def unblock_application(cls, db_session: AsyncSession, block_set_id: int, app: Application):
        block_set = await cls.get_block_set(block_set_id)
        block_set.apps.remove(app)

        await db_session.commit()
        return block_set
