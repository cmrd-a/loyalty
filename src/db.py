from sqlalchemy.ext.asyncio import create_async_engine

from config import config
from pg_service import PGService

engine = create_async_engine(f"postgresql+asyncpg://{config.pg_connection_sting}", echo=True)  # TODO: del echo
pg_service: PGService = PGService(engine)
