from sqlalchemy.orm import Session

from app.db.models import BlockSet, TimeFrame, Application
from app.db.config import LIMIT
from app.db.schemas import BlockSetCreate


class BlockSetDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_block_sets(self):
        q = await self.db_session.query(BlockSet).limit(LIMIT).all()
        return q

    async def get_block_set(self, block_set_id: int) -> BlockSet:
        q = await self.db_session.query(BlockSet) \
            .filter(BlockSet.id == block_set_id).first()
        return q

    async def create_block_set(self, block_set: BlockSetCreate):
        new_block_set = BlockSet(name=block_set.name)
        # Wie auf Applikationen verweisen?
        self.db_session.add(new_block_set)
        await self.db_session.commit()
        await self.db_session.refresh(new_block_set)
        return new_block_set

    async def add_time_frame(self, block_set_id: int, time_frame: TimeFrame):
        block_set = await self.get_block_set(block_set_id)
        block_set.time_frames.append(time_frame)
        await self.db_session.commit()
        await self.db_session.refresh(block_set)
        return block_set

    async def get_applications_by_block_set(self, block_set_id: int):
        block_set = await self.get_block_set(block_set_id)
        return block_set.apps

    async def block_application(self, block_set_id: int, app: Application):
        block_set = await self.get_block_set(block_set_id)
        block_set.apps.append(app)

        await self.db_session.commit()

    async def unblock_application(self, block_set_id: int, app: Application):
        block_set = await self.get_block_set(block_set_id)
        block_set.apps.remove(app)

        await self.db_session.commit()

