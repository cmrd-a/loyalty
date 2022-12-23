from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine

from models import AvailableCode
from utils import generate_code


class PGService:
    def __init__(self, engine: AsyncEngine):
        self.session = async_sessionmaker(engine)

    async def make_q(self):
        async with self.session() as session:
            stmt = select(AvailableCode)

            result = await session.execute(stmt)
            a1: AvailableCode = result.scalars().first()
            a1.activation_quantity = 228
            await session.commit()

    async def create_promo_code(
        self,
        code: str,
        discount_percents: int,
        activation_quantity: int,
        expired_at: datetime,
        users_ids: list[int],
    ) -> AvailableCode:
        async with self.session() as session:
            promo_code = AvailableCode(
                code=code or generate_code(),
                expired_at=expired_at,
                activation_quantity=activation_quantity,
                for_users=users_ids,
                discount_percents=discount_percents,
            )
            session.add(promo_code)
            await session.commit()
            await session.refresh(promo_code)
            return promo_code

    async def reserve_code(self):
        ...

    async def free_code(self):
        ...

    async def apply_code(self):
        ...

    async def get_user_dicount(self, user_id: int) -> int | None:
        ...
