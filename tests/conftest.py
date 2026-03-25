import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import DATABASE_URL
from app.core.database import Base, get_db
from app.main import app
from app.repositories import TeaRepository, TeaVariantRepository, TransactionRepository
from app.services import TransactionService

TEST_DATABASE_URL = DATABASE_URL.replace(
    "gucheung_am_inventory", "gucheung_am_inventory_test"
)

engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def service(db_session: AsyncSession):
    return TransactionService(
        repository=TransactionRepository(db_session),
        tea_repository=TeaRepository(db_session),
        tea_variant_repository=TeaVariantRepository(db_session),
    )
