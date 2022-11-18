from src.database import database
from src.config import postgres_env


async def on_startup() -> None:
    """
    Действия, выполняемые при запуске приложения
    """
    await database.startup(postgres_env.USER, 
                           postgres_env.PASSWORD, 
                           postgres_env.HOST, 
                           postgres_env.PORT, 
                           postgres_env.DB)
    print('App is running!')


async def on_shutdown() -> None:
    """
    Действия, выполняемые при завершении работы приложения.
    """
    print('App is shutting down!')
