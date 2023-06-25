from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


class TokenConfiguration(BaseConfig):
    secret: str = Field("fake_secret_code_fake_secret_code", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="TOKEN_ALGORITHM")


class DatabaseConfiguration(BaseConfig):
    database: str = Field("postgresql", env="DB_TYPE")
    postgres_user: str = Field("user", env="POSTGRES_USER")
    postgres_password: str = Field("qwerty123", env="POSTGRES_PASSWORD")
    postgres_host: str = Field("127.0.0.1", env="POSTGRES_HOST")
    postgress_port: int = Field(5432, env="POSTGRES_PORT")
    postgres_db: str = Field("auth_base", env="POSTGRES_DB")


class Configuration(BaseConfig):
    db: DatabaseConfiguration = DatabaseConfiguration()
    token: TokenConfiguration = TokenConfiguration()


config = Configuration()

db_url = (
    f'{config.db.database}+psycopg2://{config.db.postgres_user}:'
    f'{config.db.postgres_password}@{config.db.postgres_host}:'
    f'{config.db.postgress_port}/{config.db.postgres_db}'
)
