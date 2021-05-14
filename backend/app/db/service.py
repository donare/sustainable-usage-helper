from app.db.config import async_session, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
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
    block_set = BlockSetCreate(name="Default Block Set")

    async with async_session() as db_session:
        if len(await BlockSet.find_all(db_session)) == 0:
            new_block_set = BlockSet(block_set)
            await new_block_set.add_self(db_session)


async def get_blocked_applications(db_session: AsyncSession):
    now = dt.now()
    time_now = now.time()
    weekday = now.weekday()
    weekday_mask = 1 << weekday

    query = select(Application)\
        .join(Application.block_sets)\
        .join(BlockSet.time_frames)\
        .where(TimeFrame.start_time >= time_now)\
        .where(TimeFrame.end_time <= time_now)\
        .where(TimeFrame.weekdays & weekday_mask)

    return (await db_session.execute(query)).scalars().all()
