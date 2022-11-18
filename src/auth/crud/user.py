import asyncpg
from src.auth import dto


async def create_user(con: asyncpg.Connection, login: str, hashed_password: str) -> None:
    query = '''
    INSERT INTO users (login, hashed_password) VALUES ($1, $2);
    '''
    await con.execute(query, login, hashed_password)


async def get_user_by_login(con: asyncpg.Connection, login: str) -> dto.User:
    query = '''
    SELECT id, hashed_password, role, is_superuser FROM users WHERE login=$1;
    '''
    res = await con.fetchrow(query, login)
    return None if res is None else dto.User(**res)
