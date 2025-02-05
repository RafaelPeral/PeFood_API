import pytest
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_connect_db():
    db_handler = DBConnectionHandler()
    await db_handler.connect_db()


@pytest.mark.asyncio
async def test_get_client_uninitialized():
    db_handler = DBConnectionHandler()
    await db_handler.connect_db()
    assert db_handler.get_client() is not None


@pytest.mark.asyncio
async def test_get_db_connection_uninitialized():
    db_handler = DBConnectionHandler()
    await db_handler.connect_db()
    assert db_handler.get_db_connection() is not None
