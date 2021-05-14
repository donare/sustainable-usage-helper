from __future__ import annotations
from typing import List
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

    apps = relationship("Application", secondary=block_associations, back_populates="block_sets", lazy='selectin')
    time_frames = relationship("TimeFrame", back_populates="block_set", lazy='selectin')

    def __init__(self, block_set: BlockSetCreate):
        self.name = block_set.name
        self.apps = []
        self.time_frames = []

    @classmethod
    async def add_time_frame(cls, block_set_id: int, time_frame: TimeFrame, db_session: AsyncSession):
        block_set = await cls.find_by_id(block_set_id, db_session)
        block_set.time_frames.append(time_frame)
        await db_session.commit()
        await db_session.refresh(block_set)
        return block_set

    @classmethod
    async def remove_time_frame(cls, block_set_id: int, time_frame: TimeFrame, db_session: AsyncSession):
        block_set = await cls.find_by_id(block_set_id, db_session)
        block_set.time_frames.remove(time_frame)
        await db_session.commit()
        await db_session.refresh(block_set)
        return block_set

    @classmethod
    async def get_applications(cls, block_set_id: int, db_session) -> List[Application]:
        block_set = await cls.find_by_id(block_set_id, db_session)
        return block_set.apps

    @classmethod
    async def block_application(cls, block_set_id: int, app: Application, db_session: AsyncSession):
        block_set = await cls.find_by_id(block_set_id, db_session)
        block_set.apps.append(app)
        await db_session.commit()
        return block_set

    @classmethod
    async def unblock_application(cls, block_set_id: int, app: Application, db_session: AsyncSession):
        block_set = await cls.find_by_id(block_set_id, db_session)
        block_set.apps.remove(app)
        await db_session.commit()
        await app.delete_self(db_session)  # todo: Is this necessary or can the system the DB be set to delete orphans automatically?
        return block_set

    @classmethod
    async def find_by_id(cls, id: int, db_session: AsyncSession) -> BlockSet:
        return await super(BlockSet, cls).find_by_id(id, db_session)
