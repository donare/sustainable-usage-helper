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
