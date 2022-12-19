from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    pg_db: str = Field(env="LOYALTY_POSTGRES_DB")
    pg_user: str = Field(env="LOYALTY_POSTGRES_USER")
    pg_password: str = Field(env="LOYALTY_POSTGRES_PASSWORD")
    pg_host: str = Field(env="LOYALTY_POSTGRES_HOST")
    pg_port: int = Field(env="LOYALTY_POSTGRES_PORT")

    @property
    def pg_connection_sting(self):
        return f"{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"


config = Settings()
