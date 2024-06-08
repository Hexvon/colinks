import asyncio
from contextlib import ExitStack

import pytest
import pytest_asyncio
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from asyncpg import Connection
from httpx import AsyncClient

from colinks_backend.app import app as actual_app
from colinks_backend.db import Base
from colinks_backend.db.engine import get_db_session, DatabaseSessionManager
from test_config import TEST_CONFIG


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield actual_app


@pytest.fixture()
def create_test_async_client(app) -> AsyncClient:
    client = AsyncClient(app=app, base_url="http://127.0.0.1")
    client.headers["origin"] = "http://127.0.0.1"
    client.headers["referer"] = "http://127.0.0.1/"
    return client


def run_migrations(connection: Connection):
    config = Config("CoLinks/alembic.ini")
    config.set_main_option("script_location", "../src/migrations")
    config.set_main_option("sqlalchemy.url", TEST_CONFIG.test_database_url)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session")
async def sessionmanager(event_loop):
    return DatabaseSessionManager(TEST_CONFIG.test_database_url, {"echo": TEST_CONFIG.echo_sql})


@pytest.fixture(scope="session", autouse=True)
async def setup_database(sessionmanager: DatabaseSessionManager):
    # Run alembic migrations on test DB
    async with sessionmanager.connect() as connection:
        await connection.run_sync(run_migrations)

    yield

    # Teardown
    await sessionmanager.close()


# Each test function is a clean slate
@pytest.fixture(scope="function")
async def transactional_session(sessionmanager):
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, db_session):
    async def get_db_session_override():
        yield db_session

    app.dependency_overrides[get_db_session] = get_db_session_override
