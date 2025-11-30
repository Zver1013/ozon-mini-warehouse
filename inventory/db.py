from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/miniwarehouse"

# создаём движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# базовый класс для ORM-моделей
class Base(DeclarativeBase):
    pass

# удобная фикстура для получения сессии
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
