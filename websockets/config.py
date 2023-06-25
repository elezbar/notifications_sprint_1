from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = "./.env"
        env_nested_delimiter = "__"


class TokenConfiguration(BaseConfig):
    secret: str = Field("fake_secret_code_fake_secret_code", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="TOKEN_ALGORITHM")
