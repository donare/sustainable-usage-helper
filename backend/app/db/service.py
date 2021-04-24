
from app.db import models, schemas
from app.db.config import async_session
from app.db.dao.application import ApplicationDAO
from app.db.dao.timeframe import TimeFrameDAO
from app.db.dao.blockset import BlockSetDAO
from sqlalchemy.future import select

from app.db.models import Application, BlockSet, TimeFrame


from datetime import datetime as dt


async def get_applications_by_block_set(block_set_id: int):
    async with async_session() as session:
        block_set_dao = BlockSetDAO(session)

        return await block_set_dao.get_applications_by_block_set(block_set_id)


async def get_blocked_applications():
    now = dt.now()
    time_now = now.time()
    weekday = now.weekday()
    weekday_mask = 1 << weekday

    async with async_session() as session:
        query = select(Application)\
            .join(Application.block_sets)\
            .join(BlockSet.time_frames)\
            .filter(TimeFrame.start_time >= time_now)\
            .filter(TimeFrame.end_time <= time_now)\
            .filter(TimeFrame.weekdays & weekday_mask)

        return await session.execute(query).all()


async def get_time_frames_by_block_set(block_set_id: int):
    async with async_session() as session:
        query = select(BlockSet)\
            .join(BlockSet.time_frames)\
            .filter(BlockSet.id == block_set_id)

        return await session.execute(query).all()


async def block_application(app_id: int, block_set_id: int):
    async with async_session() as session:
        app_dao = ApplicationDAO(session)
        block_set_dao = BlockSetDAO(session)

        app = await app_dao.get_application(app_id)
        await block_set_dao.block_application(block_set_id, app)


async def unblock_application(app_id, block_set_id):
    async with async_session() as session:
        app_dao = ApplicationDAO(session)
        block_set_dao = BlockSetDAO(session)

        app = await app_dao.get_application(app_id)
        await block_set_dao.unblock_application(block_set_id, app)

        # Todo: Is explicit deletion of orphans necessary? Or can this be set done automatically?
