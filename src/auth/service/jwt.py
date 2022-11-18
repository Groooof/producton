import datetime as dt
import uuid
import asyncpg

from src.auth import crud
from src import config
from src.auth import utils
from src.auth import exceptions as exc
from src.utils.crypto import generate_uuid
from src.utils.converters import _dt


async def create_refresh_token(con: asyncpg.Connection, user_id: int, token: uuid.UUID) -> None:
    await crud.create_refresh_token(con, user_id, token, dt.datetime.now() + config.JWT_RT_LIFETIME)


def generate_jwt_refresh() -> uuid.UUID:
    return generate_uuid()

    
def generate_jwt_access(user_id: str, role: str, is_superuser: bool) -> str:
    jwt = utils.JWTToken()
    jwt.header['alg'] = 'HS256'
    jwt.header['typ'] = 'JWT'
    jwt.payload['sub'] = user_id
    jwt.payload['role'] = role
    jwt.payload['is_superuser'] = is_superuser
    jwt.payload['exp'] = _dt.to_timestamp(dt.datetime.now() + config.JWT_AT_LIFETIME)
    jwt.sign(config.jwt_env.SECRET)
    return str(jwt)


async def verify_refresh_token(con: asyncpg.Connection, user_id: int, token: uuid.UUID) -> None:
    is_valid = await crud.verify_refresh_token(con, user_id, token)
    if not is_valid:
        raise exc.INVALID_TOKEN


async def update_refresh_token(con: asyncpg.Connection, token: uuid.UUID, new_token: uuid.UUID) -> None:
    new_expires = dt.datetime.now() + config.JWT_RT_LIFETIME
    await crud.update_refresh_token(con, token, new_token, new_expires)
   
   
async def delete_refresh_token(con: asyncpg.Connection, token: uuid.UUID):
    await crud.delete_refresh_token(con, token)
    