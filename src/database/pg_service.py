import uuid
from datetime import datetime

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config
from database.models import PromoCode, PromoCodeStatus, CodeStatus
from utils import generate_code


class PGService:
    def __init__(self):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{config.pg_connection_sting}", echo=True
        )  # TODO: del echo
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_promo_code(
        self,
        code: str,
        discount_percents: int,
        activation_quantity: int,
        expired_at: datetime,
        users_ids: list[int],
    ) -> PromoCode:
        #  проверка, что не существует такого же активного(constraint?)
        async with self.session() as session:
            promo_code = PromoCode(
                code=code or generate_code(),
                expired_at=expired_at,
                activation_quantity=activation_quantity,
                users_ids=users_ids,
                discount_percents=discount_percents,
            )
            session.add(promo_code)
            await session.commit()
            return promo_code

    async def get_promo_codes(self, code: str) -> list[PromoCode]:
        async with self.session() as session:
            query = select(PromoCode).where(PromoCode.code == code)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_promo_code_statuses(self, promo_codes: list[PromoCode], user_id: int) -> list[PromoCodeStatus]:
        async with self.session() as session:
            query = (
                select(PromoCodeStatus)
                .where(PromoCodeStatus.code_id.in_([pc.id for pc in promo_codes]))
                .where(PromoCodeStatus.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()

    async def reserve_promo_code(self, code_id: uuid.UUID, user_id: int) -> PromoCodeStatus:
        async with self.session() as session:
            promo_code_status = PromoCodeStatus(code_id=code_id, user_id=user_id, status=CodeStatus.reserved)
            session.add(promo_code_status)
            await session.commit()
            return promo_code_status

    async def free_promo_code(self, reserve_id: uuid.UUID):
        async with self.session() as session:
            query = (
                select(PromoCodeStatus)
                .where(PromoCodeStatus.id == reserve_id)
                .where(PromoCodeStatus.status == CodeStatus.reserved)
            )
            result = await session.execute(query)
            promo_code_reserved: PromoCodeStatus = result.scalars().first()
            if promo_code_reserved.created_at:
                pass
            await session.execute(delete(PromoCodeStatus).where(PromoCodeStatus.id == reserve_id))
            await session.commit()

    async def apply_promo_code(self, reserve_id):
        async with self.session() as session:
            query = update(PromoCodeStatus).where(PromoCodeStatus.id == reserve_id).values(status=CodeStatus.applied)
            await session.execute(query)
            await session.commit()

    async def get_user_dicount(self, user_id: int) -> int | None:
        ...


pg_service = PGService()
