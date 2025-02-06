import pytest
from pydantic import ValidationError
from src.model.entities.address import Address
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_valid_address():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    address = await Address(
        street="Avenida Paulista",
        number=1000,
        city="São Paulo",
        neighborhood="Brás",
        zip_code=12345678,
        complement="Apt 101",
        reference="Near the store",
    ).insert()
    assert address.street == "Avenida Paulista"
    assert address.number == 1000
    assert address.city == "São Paulo"
    assert address.neighborhood == "Brás"
    assert address.zip_code == 12345678
    assert address.complement == "Apt 101"
    assert address.reference == "Near the store"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_zip_code_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Address(
            street="Rua A",
            number=10,
            city="Cidade",
            neighborhood="Bairro",
            zip_code=123,
        )
    assert "ZIP Code must have 5 or 8 digits" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_city_name():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Address(
            street="Rua A",
            number=10,
            city="C1dade",
            neighborhood="Bairro",
            zip_code=12345,
        )
    assert "The field must contain only letters" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_street_name():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Address(
            street="Rua 123",
            number=10,
            city="Cidade",
            neighborhood="Bairro",
            zip_code=12345,
        )
    assert "The field must contain only letters" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_neighborhood_name():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Address(
            street="Rua A",
            number=10,
            city="Cidade",
            neighborhood="B@irro",
            zip_code=12345,
        )
    assert "The field must contain only letters" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_alias_generator():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert Address.Settings.alias_generator("AddressField") == "addressfield"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_schema_extra():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert Address.Settings.schema_extra == {
        "example": {
            "street": "Avenida Paulista",
            "number": 1000,
            "city": "São Paulo",
            "neighborhood": "Brás",
            "zip_code": 12345,
            "complement": "Apt 101",
            "reference": "Near the store",
        }
    }
    await db_handler.disconnect_db()
