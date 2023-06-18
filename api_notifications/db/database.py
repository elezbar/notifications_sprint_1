
from core.config import settings
from pyparsing import Generator
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

engine: AsyncEngine = create_async_engine(
    settings.db_url
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> Generator:
    async with async_session() as session:
        await session.execute("set timezone = 'Europe/Moscow';")
        yield session
