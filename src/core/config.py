from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    pg_db: str = Field(env="LOYALTY_POSTGRES_DB")
    pg_user: str = Field(env="LOYALTY_POSTGRES_USER")
    pg_password: str = Field(env="LOYALTY_POSTGRES_PASSWORD")
    pg_host: str = Field(env="LOYALTY_POSTGRES_HOST")
    pg_port: int = Field(env="LOYALTY_POSTGRES_PORT")

    reserve_timeout_seconds: int = Field(env="RESERVE_TIMEOUT_SECONDS", default=900)
    notifier_api_url: str = Field(env="NOTIFIER_API_URL", default="http://localhost")
    app_listen_port: int = Field(env="LOYALTY_LISTEN_PORT", default=50051)

    @property
    def common_pg_uri(self):
        return f"{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"

    @property
    def app_pg_uri(self):
        return f"postgresql+asyncpg://{self.common_pg_uri}"

    @property
    def alembic_pg_uri(self):
        return f"postgresql+psycopg://{self.common_pg_uri}"


config = Settings()
