import uuid
from datetime import datetime
import enum
from sqlalchemy import String, DateTime, text, Integer, SmallInteger, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from config import config


@enum.unique
class CodeStatus(enum.Enum):
    reserved = "reserved"
    applied = "applied"


@enum.unique
class Operations(enum.Enum):
    reserve = "reserve"
    apply = "apply"
    free = "free"


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(True), primary_key=True, default=uuid.uuid4, server_default=text("public.uuid_generate_v4()")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(True), default=datetime.utcnow, server_default=func.CURRENT_TIMESTAMP()
    )


class AvailableCode(Base):
    __tablename__ = "available_codes"

    code: Mapped[str] = mapped_column(String(24), nullable=False, index=True, unique=True)
    expired_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    activation_quantity: Mapped[int] = mapped_column(SmallInteger(), default=1, server_default="1", nullable=False)
    for_users: Mapped[list[int]] = mapped_column(
        ARRAY(Integer()), server_default=text("ARRAY[]::integer[]"), nullable=False
    )
    discount_percents: Mapped[int] = mapped_column(SmallInteger(), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code!r}, {self.discount_percents!r})"


class UsedCode(Base):
    __tablename__ = "used_codes"

    code: Mapped[str] = mapped_column(String(24), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    status: Mapped[str] = mapped_column(ENUM(CodeStatus, name="status"))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code!r}, {self.user_id!r}, {self.status!r})"


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
    operation: Mapped[str] = mapped_column(ENUM(Operations, name="operation"))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.code!r}, {self.user_id!r})"


async def connect_to_pg():
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.pg_connection_sting}",
        # echo=True
    )
    async with engine.begin() as conn:
        # await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;'))
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        return conn
