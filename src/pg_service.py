from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine

from models import AvailableCode


class PGService:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def make_q(self):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(AvailableCode)

            result = await session.execute(stmt)
            a1: AvailableCode = result.scalars().first()
            a1.activation_quantity = 228
            await session.commit()