from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status

from app.db.config import LIMIT


@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    async def add_self(self, db_session: AsyncSession):
        try:
            db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self)
            return self
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    async def delete_self(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @classmethod
    async def find_all(cls, db_session: AsyncSession):
        q = select(cls).limit(LIMIT)
        result = await db_session.execute(q)
        instance = result.scalars().all()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Record not found": f"There are no entries in table \"{cls.__tablename__}\"."}
            )
        else:
            return instance

    @classmethod
    async def find_by_id(cls, id: int, db_session: AsyncSession):
        q = select(cls).where(cls.id == id)
        r = await db_session.execute(q)
        instance = r.scalars().first()

        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"Record not found": f"Entry with id {id} not in table \"{cls.__tablename__}\"."}
            )
        else:
            return instance
