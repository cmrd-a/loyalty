import uuid
import datetime

import pytz
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config
from database.models import PromoCode, PromoCodeStatus, CodeStatus, PromoCodeStatusLog, CodeOperation, UserDiscount
from utils import generate_code


class DBService:
    def __init__(self):
        self.engine = create_async_engine(config.app_pg_uri)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_promo_code(
        self,
        code: str,
        discount_percents: int,
        expired_at: datetime.datetime,
        users_ids: list[int],
    ) -> PromoCode:
        async with self.session() as session:
            promo_code = PromoCode(
                code=code or generate_code(),
                expired_at=expired_at,
                users_ids=users_ids,
                discount_percents=discount_percents,
            )
            session.add(promo_code)
            await session.commit()
            return promo_code

    async def get_promo_code_by_id(self, id_: uuid.UUID) -> PromoCode:
        async with self.session() as session:
            query = select(PromoCode).where(PromoCode.id == id_)
            result = await session.execute(query)
            return result.scalars().first()

    async def get_promo_codes_by_code(self, code: str) -> list[PromoCode]:
        async with self.session() as session:
            query = select(PromoCode).where(PromoCode.code == code).order_by(PromoCode.created_at.desc())
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

    async def reserve_promo_code(self, promo_code: PromoCode, user_id: int) -> PromoCodeStatus:
        async with self.session() as session:
            promo_code_status = PromoCodeStatus(code_id=promo_code.id, user_id=user_id, status=CodeStatus.reserved)
            session.add(promo_code_status)
            await session.commit()
            return promo_code_status

    async def free_promo_code(self, reserve_id: uuid.UUID) -> None:
        async with self.session() as session:
            await session.execute(delete(PromoCodeStatus).where(PromoCodeStatus.id == reserve_id))
            await session.commit()

    async def apply_promo_code(self, reserve_id) -> None:
        async with self.session() as session:
            query = update(PromoCodeStatus).where(PromoCodeStatus.id == reserve_id).values(status=CodeStatus.applied)
            await session.execute(query)
            await session.commit()

    async def get_promo_code_status(self, status_id: uuid.UUID) -> PromoCodeStatus:
        async with self.session() as session:
            query = select(PromoCodeStatus).where(PromoCodeStatus.id == status_id)
            result = await session.execute(query)
            return result.scalars().first()

    async def create_promo_code_status_log(self, code: str, operation: CodeOperation, user_id: int = None) -> None:
        async with self.session() as session:
            log = PromoCodeStatusLog(code=code, operation=operation, user_id=user_id)
            session.add(log)
            await session.commit()

    async def create_user_dicount(
        self, user_id: int, discount_percents: int, expired_at: datetime.datetime
    ) -> UserDiscount:
        async with self.session() as session:
            user_discount = UserDiscount(user_id=user_id, discount_percents=discount_percents, expired_at=expired_at)
            session.add(user_discount)
            await session.commit()
            return user_discount

    async def get_user_discount(self, user_id: int) -> UserDiscount:
        async with self.session() as session:
            query = select(UserDiscount).where(UserDiscount.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().first()

    async def delete_user_discount(self, discount_id: uuid.UUID) -> None:
        async with self.session() as session:
            await session.execute(delete(UserDiscount).where(UserDiscount.id == discount_id))
            await session.commit()


db_svc = DBService()
