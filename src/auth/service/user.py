import typing as tp
import asyncpg

from src.auth import crud
from src.auth import utils
from src.auth.dto import User
from src.auth import exceptions as exc


async def create_user(con: asyncpg.Connection, login: str, password: str) -> None:
    hashed_password = utils.PasswordHasher.hash(password)
    
    try:
        await crud.create_user(con, login, hashed_password)
    except asyncpg.exceptions.UniqueViolationError:
        raise exc.USER_ALREARY_EXISIS
    

async def verify_user(con: asyncpg.Connection, login: str, password: str) -> tp.Optional[User]:
    user = await crud.get_user_by_login(con, login)
    
    if user is None:
        raise exc.INVALID_CLIENT
    
    if not utils.PasswordHasher.verify(password, user.hashed_password):
        raise exc.INVALID_CLIENT
    return user
