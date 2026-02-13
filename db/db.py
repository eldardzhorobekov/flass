import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "db")  # Именно "db", как в docker-compose
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
# 1. Создаем движок (Engine)
# echo=True полезен на локалке, чтобы видеть SQL-запросы в консоли
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Проверяет живое ли соединение перед использованием
)

# 2. Создаем фабрику сессий
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# 3. Функция-помощник (Dependency) для получения сессии
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
