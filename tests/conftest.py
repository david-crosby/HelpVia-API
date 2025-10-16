"""Shared pytest fixtures"""
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.main import app
from app.models.user import User

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_db):
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session):
    user = User(username="testuser", email="test@example.com", hashed_password=get_password_hash("testpassword"), full_name="Test User")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def auth_token(client, test_user):
    response = await client.post("/api/v1/auth/login", data={"username": "testuser", "password": "testpassword"})
    return response.json()["access_token"]

@pytest.fixture
async def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
