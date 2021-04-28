from typing import AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./settings.db"

LIMIT = 100

engine = create_async_engine(
    DATABASE_URL, future=True
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,  # entities available after commit
    class_=AsyncSession  #
)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    session = async_session()
    try:
        yield session
        await session.commit()
    except SQLAlchemyError as ex:
        await session.rollback()
        raise ex
    finally:
        await session.close()
