import datetime as dt
import uuid
import asyncpg


async def create_refresh_token(con: asyncpg.Connection, user_id: int, token: str, expires: dt.datetime) -> None:
    query = '''
    INSERT INTO refresh_tokens (user_id, token, expires) VALUES ($1, $2, $3);
    '''
    await con.execute(query, user_id, token, expires)
    
    
async def update_refresh_token(con: asyncpg.Connection, token: uuid.UUID, new_token: uuid.UUID, new_expires: dt.datetime) -> None:
    query = '''
    UPDATE refresh_tokens SET token=$2, expires=$3 WHERE token=$1;
    '''
    await con.execute(query, token, new_token, new_expires)
    
    
async def verify_refresh_token(con: asyncpg.Connection, user_id: int, token: uuid.UUID) -> bool:
    query = '''
    SELECT EXISTS (SELECT 1 FROM refresh_tokens WHERE user_id=$1 AND token=$2 AND expires>=NOW());
    '''
    return await con.fetchval(query, user_id, token)


async def delete_refresh_token(con: asyncpg.Connection, token: uuid.UUID) -> None:
    query = '''
    DELETE FROM refresh_tokens WHERE token=$1;
    '''
    await con.execute(query, token)
