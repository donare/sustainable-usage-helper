from app.db.config import async_session, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dao.application import ApplicationDAO
from app.db.dao.timeframe import TimeFrameDAO
from app.db.dao.blockset import BlockSetDAO
from sqlalchemy.future import select

from app.db.schemas import BlockSetCreate
from app.db.models.application import Application
from app.db.models.blockset import BlockSet
from app.db.models.timeframe import TimeFrame

from datetime import datetime as dt


async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_defaults():
    async with async_session() as session:
        block_set_dao = BlockSetDAO(session)
        block_set = BlockSetCreate(name="Default Block Set")

        if len(await block_set_dao.get_all_block_sets()) == 0:
            new_block_set = await block_set_dao.create_block_set(block_set)


async def create_block_set(block_set: BlockSetCreate):
    async with async_session() as session:
        block_set_dao = BlockSetDAO(session)

        bs = await block_set_dao.create_block_set(block_set)

        return list(bs[0])


async def get_all_block_sets(session: AsyncSession):
    block_set_dao = BlockSetDAO(session)
    return await block_set_dao.get_all_block_sets()


async def get_block_set(block_set_id: int):
    async with async_session() as session:
        block_set_dao = BlockSetDAO(session)

        return await block_set_dao.get_block_set(block_set_id)


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
