from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.config import Base
from app.db.models.base import BaseMixin
from app.db.models.associations import block_associations
from app.db.schemas import ApplicationCreate


class Application(Base, BaseMixin):
    app_path = Column(String, unique=True, index=True)

    block_sets = relationship("BlockSet", secondary=block_associations, back_populates="application", lazy='selectin')

    def __init__(self, app: ApplicationCreate):
        self.app_path = app.app_path

    @classmethod
    async def find_by_path(cls, db_session: AsyncSession, app_path: str):
        q = select(cls).where(cls.app_path == app_path)
        r = await db_session.execute(q)

        return r.scalars().first()