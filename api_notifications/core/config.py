import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    host: str = Field('127.0.0.1', env='HOST')
    port: int = int(Field('9080', env='PORT'))
    project_name: str = Field('notification', env='PROJECT_NAME')
    name_instant_queues: str = Field('instant', env='NAME_INSTANT_QUEUE')
    name_delayed_queues: str = Field('delayed', env='NAME_DELAYED_QUEUE')
    broker_login: str = Field('guest', env='BROKER_LOGIN')
    broker_password: str = Field('guest', env='BROKER_PASSWORD')
    broker_host: str = Field('127.0.0.1', env='BROKER_HOST')
    broker_port: int = int(Field('5672', env='BROKER_PORT'))
    auth_url: str = Field('auth_service', env='AUTH_URL')
    db_url = (
        f"{Field('postgresql', env='DB_TYPE')}+psycopg2://{Field('user', env='POSTGRES_USER')}:"
        f"{Field('123qwe', env='POSTGRES_PASSWORD')}@{Field('guest', env='POSTGRES_HOST')}:"
        f"{Field(5432, env='POSTGRES_PORT')}/{Field('notification', env='POSTGRES_DB')}"
    )

    class Config:
        env_file = '../../../.env'
        env_file_encoding = 'utf-8'


settings = Settings.construct()
