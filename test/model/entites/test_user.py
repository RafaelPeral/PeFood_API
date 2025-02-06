import pytest
from pydantic import ValidationError
from src.model.entities.user import User
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_valid_user():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    user = await User(
        name="John Doe",
        email="johndoe@example.com",
        password="SecureP@ss123",
        phone="1234567890",
    ).insert()
    assert user.name == "John Doe"
    assert user.email == "johndoe@example.com"
    assert len(user.password) > 0
    assert user.phone == "1234567890"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_name_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        User(
            name="Jo",
            email="johndoe@example.com",
            password="SecureP@ss123",
            phone="1234567890",
        )
    assert "Name must be at least 3 characters long" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_name_characters():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        User(
            name="John123",
            email="johndoe@example.com",
            password="SecureP@ss123",
            phone="1234567890",
        )
    assert "Name cannot contain numbers or special characters" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_phone_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        User(
            name="John Doe",
            email="johndoe@example.com",
            password="SecureP@ss123",
            phone="123",
        )
    assert "Phone number must be between 10 and 15 digits long" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_phone_characters():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        User(
            name="John Doe",
            email="johndoe@example.com",
            password="SecureP@ss123",
            phone="12A4567890",
        )
    assert "Phone number must contain only digits" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_password_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        User(
            name="John Doe",
            email="johndoe@example.com",
            password="Short1!",
            phone="1234567890",
        )
    assert "Password must be at least 8 characters long" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_alias_generator():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert User.Settings.alias_generator("UserEmail") == "useremail"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_schema_extra():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert User.Settings.schema_extra == {
        "example": {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "SecureP@ss123",
            "addresses": [
                {
                    "street": "Fifth Avenue",
                    "number": 1000,
                    "city": "New York",
                    "neighborhood": "Manhattan",
                    "zip_code": 10001,
                    "complement": "Apt 101",
                    "reference": "Near the shopping mall",
                }
            ],
            "phone": "1234567890",
            "payment_formats": [
                {"id": "65d1b5e5f3a3b8b7e2f8c4a1", "name": "Cash"},
                {"id": "65d1b5e5f3a3b8b7e2f8c4a2", "name": "Credit Card"},
                {"id": "65d1b5e5f3a3b8b7e2f8c4a3", "name": "Debit Card"},
            ],
        }
    }
    await db_handler.disconnect_db()
