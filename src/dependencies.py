from src.database import database
from fastapi import Depends
import asyncpg


def get_db_connection(con: asyncpg.Connection = Depends(database.connection)):
    """
    Зависимость (в контексте fastapi) для удобного подключения к бд
    :param con:
    :return:
    """
    return con
