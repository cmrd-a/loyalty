import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import config


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(True), primary_key=True, default=uuid.uuid4, server_default=text("public.uuid_generate_v4()")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(True), default_factory=datetime.utcnow)


class AvailableCode(Base):
    __tablename__ = "available_codes"

    code: Mapped[str] = mapped_column(String(24))


async def make_eng():
    engine = create_async_engine(f"postgresql+asyncpg://{config.pg_connection_sting}", echo=True)
    async with engine.begin() as conn:
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;'))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
