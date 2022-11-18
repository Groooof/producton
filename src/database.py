from abc import ABCMeta, abstractmethod
import typing as tp
import asyncpg


def get_postgres_dsn(user: str, password: str, host: str, port: str, db: str,
                     sa_driver: str = None, sa_dialect: str = None):
    """
    Генерация ссылки для подключения к бд.
    """
    dsn_without_prefix = f'{user}:{password}@{host}:{port}/{db}'

    if sa_driver is None and sa_dialect is None:
        base_prefix = 'postgres://'
        return base_prefix + dsn_without_prefix

    sa_prefix = f'{sa_driver}+{sa_dialect}://'
    return sa_prefix + dsn_without_prefix


class IDatabase(metaclass=ABCMeta):

    @abstractmethod
    async def startup(self, user: str, password: str, host: str, port: str, db: str) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

    @abstractmethod
    async def connection(self):
        pass


class ASPGDatabase(IDatabase):
    def __init__(self):
        self.pool: tp.Optional[asyncpg.Pool] = None

    async def startup(self, user: str, password: str, host: str, port: str, db: str) -> None:
        """
        Создание асинхронного пула подключений к бд.
        """
        self.pool = await asyncpg.create_pool(get_postgres_dsn(user, password, host, port, db), timeout=5)

    async def shutdown(self) -> None:
        """
        Закрытие пула подключений.
        """
        await self.pool.close()

    async def connection(self) -> asyncpg.Connection:
        """
        Получение подключения из пула.
        """
        if self.pool is None:
            raise NotImplementedError('DB pool must be created first')
        con = await self.pool.acquire()
        try:
            yield con
        finally:
            await self.pool.release(con)


database = ASPGDatabase()
