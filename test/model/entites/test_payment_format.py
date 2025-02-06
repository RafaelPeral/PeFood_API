import pytest
from pydantic import ValidationError
from src.model.entities.payment_format import PaymentFormat
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_valid_payment_format():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    payment_format = await PaymentFormat(name="Credit Card").insert()
    assert payment_format.name == "Credit Card"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_valid_payment_format_with_accent():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    payment_format = await PaymentFormat(name="Cartão de Crédito").insert()
    assert payment_format.name == "Cartão de Crédito"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_valid_payment_format_with_spaces():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    payment_format = await PaymentFormat(name="  Cash On Delivery  ").insert()
    assert payment_format.name == "Cash On Delivery"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_name_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        PaymentFormat(name="CC")
    assert "The payment method name must be at least 3 characters long" in str(
        excinfo.value
    )
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_characters_numbers():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        PaymentFormat(name="Cash123")
    assert (
        "The payment method name cannot contain numbers or special characters"
        in str(excinfo.value)
    )
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_characters_special():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        PaymentFormat(name="Cash@#$")
    assert (
        "The payment method name cannot contain numbers or special characters"
        in str(excinfo.value)
    )
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_empty_name():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        PaymentFormat(name="")
    assert "The payment method name must be at least 3 characters long" in str(
        excinfo.value
    )
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_name_only_spaces():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        PaymentFormat(name="   ")
    assert "The payment method name must be at least 3 characters long" in str(
        excinfo.value
    )
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_alias_generator():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert PaymentFormat.Settings.alias_generator("PaymentMethod") == "paymentmethod"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_schema_extra():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert PaymentFormat.Settings.schema_extra == {
        "example": {
            "name": "Cash",
        }
    }
    await db_handler.disconnect_db()
