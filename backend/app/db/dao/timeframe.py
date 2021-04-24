from sqlalchemy.orm import Session

from app.db.models import TimeFrame
from app.db.config import LIMIT
from app.db.schemas import TimeFrameCreate


class TimeFrameDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_time_frame(self, time_frame_id: int) -> TimeFrame:
        q = await self.db_session.query(TimeFrame)\
            .filter(TimeFrame.id == time_frame_id).first()
        return q
    
    async def get_time_frames(self):
        q = await self.db_session.query(TimeFrame).limit(LIMIT).all()
        return q

    async def create_time_frame(self, time_frame: TimeFrameCreate):
        new_time_frame = TimeFrame(**time_frame.dict())
        self.db_session.add(new_time_frame)
        await self.db_session.commit()
        await self.db_session.refresh(new_time_frame)
        return new_time_frame

    async def remove_time_frame(self, time_frame_id: int):
        time_frame = self.get_time_frame(time_frame_id)
        self.db_session.delete(time_frame)
        await self.db_session.commit()
