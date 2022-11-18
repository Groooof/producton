from pydantic import BaseSettings
import datetime as dt
import pathlib


class BaseEnv(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PostgresEnv(BaseEnv):
    """
    Переменные окружения.
    """
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: str

    class Config:
        env_prefix = 'POSTGRES_'


class JWTEnv(BaseEnv):
    SECRET: str

    class Config:
        env_prefix = 'JWT_'
    

postgres_env = PostgresEnv()
jwt_env = JWTEnv()
JWT_AT_LIFETIME = dt.timedelta(minutes=59)
JWT_RT_LIFETIME = dt.timedelta(days=7)
JWT_AT_TYPE = 'bearer'
