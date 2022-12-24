import uuid
from datetime import datetime
import enum
from sqlalchemy import String, DateTime, text, Integer, SmallInteger, func, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


from config import config


@enum.unique
class CodeStatus(enum.Enum):
    reserved = "reserved"
    applied = "applied"


@enum.unique
class CodeOperation(enum.Enum):
    reserve = "reserve"
    apply = "apply"
    free = "free"


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, server_default=text("public.uuid_generate_v4()"))
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default=func.CURRENT_TIMESTAMP())

    __mapper_args__ = {"eager_defaults": True}


class PromoCode(Base):
    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    users_ids: Mapped[list[int]] = mapped_column(
        ARRAY(Integer()), server_default=text("ARRAY[]::integer[]"), nullable=False
    )
    discount_percents: Mapped[int] = mapped_column(SmallInteger(), nullable=False)

    statuses: Mapped[list["PromoCodeStatus"]] = relationship(back_populates="promo_code", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code!r}, {self.discount_percents!r})"


class PromoCodeStatus(Base):
    __tablename__ = "promo_codes_statuses"

    code_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("promo_codes.id"))
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    status: Mapped[str] = mapped_column(ENUM(CodeStatus, name="status"))

    promo_code: Mapped["PromoCode"] = relationship(back_populates="statuses")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user_id!r}, {self.status!r})"


class UserDiscount(Base):
    __tablename__ = "user_discounts"

    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    discount_percents: Mapped[int] = mapped_column(SmallInteger(), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.user_id!r}, {self.discount_percents!r})"


class Log(Base):
    __tablename__ = "logs"

    code: Mapped[str] = mapped_column(String(24), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    operation: Mapped[str] = mapped_column(ENUM(CodeOperation, name="operation"))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code!r}, {self.user_id!r})"


async def connect_to_pg():
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.pg_connection_sting}",
        # echo=True
    )
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;'))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)