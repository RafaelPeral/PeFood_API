import pytest
from pydantic import ValidationError
from src.model.entities.product import Product
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_valid_product():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    product = await Product(
        name="Laptop",
        description="A high-performance laptop with 16GB RAM.",
        price=1299.99,
        images=["https://example.com/laptop.jpg"],
        categories=["Electronics"],
    ).insert()
    assert product.name == "Laptop"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_product_name_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="PC",
            description="Good PC",
            price=500.00,
            images=[],
            categories=["Computers"],
        )
    assert "The product name must be at least 3 characters long" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_product_name_special_characters():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="Laptop@#",
            description="Powerful laptop",
            price=1500.00,
            images=[],
            categories=["Electronics"],
        )
    assert "The product name cannot contain special characters" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_description_length():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="Phone",
            description="Short",
            price=800.00,
            images=[],
            categories=["Mobiles"],
        )
    assert "The description must be at least 10 characters long" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_price():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="Tablet",
            description="A nice tablet",
            price=-50.00,
            images=[],
            categories=["Electronics"],
        )
    assert "The price must be greater than zero" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_image_url():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="TV",
            description="Smart TV",
            price=1200.00,
            images=["invalid_url"],
            categories=["Electronics"],
        )
    assert "Invalid image URL" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_max_images():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="Monitor",
            description="4K monitor",
            price=500.00,
            images=[
                "https://example.com/img1.jpg",
                "https://example.com/img2.jpg",
                "https://example.com/img3.jpg",
                "https://example.com/img4.jpg",
                "https://example.com/img5.jpg",
                "https://example.com/img6.jpg",
            ],
            categories=["Electronics"],
        )
    assert "A product can have a maximum of 5 images" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_empty_categories():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    with pytest.raises(ValidationError) as excinfo:
        Product(
            name="Speaker",
            description="Wireless speaker",
            price=99.99,
            images=[],
            categories=[],
        )
    assert "The product must have at least one category" in str(excinfo.value)
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_alias_generator():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert Product.Settings.alias_generator("ProductName") == "productname"
    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_beanie_schema_extra():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()
    assert Product.Settings.schema_extra == {
        "example": {
            "name": "Product X",
            "description": "Description of product X",
            "price": 19.99,
            "images": [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg",
            ],
            "categories": ["Category A", "Category B"],
        }
    }
    await db_handler.disconnect_db()
