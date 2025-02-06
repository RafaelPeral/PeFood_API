import pytest
from pydantic import ValidationError
from src.model.entities.bag import Bag
from src.model.entities.bag import ProductItem
from src.model.entities.product import Product
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat
from src.model.entities.user import User
from src.model.settings.db_connection_handler import DBConnectionHandler

pytest_plugins = "pytest_asyncio"


@pytest.mark.asyncio
async def test_valid_bag_creation():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()

    user = User(
        name="John Doe",
        email="johndoe@example.com",
        password="SecureP@ss123",
        phone="1234567890",
    )
    product = Product(
        name="Laptop",
        description="A high-performance laptop with 16GB RAM.",
        price=1299.99,
        images=["https://example.com/laptop.jpg"],
        categories=["Electronics"],
    )
    payment_format = PaymentFormat(name="Cash")
    address = Address(
        street="Paulista Avenue",
        number=1000,
        city="São Paulo",
        neighborhood="Brás",
        zip_code=12345,
        complement="Apt 101",
        reference="Near the store",
    )
    product_item = ProductItem(quantity=1, product=product)

    bag = Bag(
        user=user,
        products=[product_item],
        address=address,
        payment_format=payment_format,
    )
    await bag.insert()

    assert bag.user.name == "John Doe"
    assert len(bag.products) == 1
    assert bag.products[0].product.name == "Laptop"
    assert bag.address.street == "Paulista Avenue"
    assert bag.payment_format.name == "Cash"

    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_bag_empty_product_list():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()

    user = User(
        name="John Doe",
        email="johndoe@example.com",
        password="SecureP@ss123",
        phone="1234567890",
    )
    payment_format = PaymentFormat(name="Cash")
    address = Address(
        street="Paulista Avenue",
        number=1000,
        city="São Paulo",
        neighborhood="Brás",
        zip_code=12345,
        complement="Apt 101",
        reference="Near the store",
    )

    with pytest.raises(ValidationError) as excinfo:
        Bag(user=user, products=[], address=address, payment_format=payment_format)
    assert "The product list cannot be empty" in str(excinfo.value)

    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_invalid_product_quantity():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()

    product = Product(
        name="Laptop",
        description="A high-performance laptop with 16GB RAM.",
        price=1299.99,
        images=["https://example.com/laptop.jpg"],
        categories=["Electronics"],
    )

    with pytest.raises(ValueError) as excinfo:
        ProductItem(quantity=1001, product=product)
    assert "The quantity of a single product cannot exceed 1000 units" in str(
        excinfo.value
    )

    await db_handler.disconnect_db()


@pytest.mark.asyncio
async def test_bag_schema_extra():
    db_handler = DBConnectionHandler()
    await db_handler.test_connect_db()

    assert Bag.Settings.schema_extra == {
        "example": {
            "user": {
                "name": "Rafael Peral",
                "email": "7tqZS@example.com",
                "password": "123456",
                "addresses": [
                    {
                        "street": "Paulista Avenue",
                        "number": 1000,
                        "city": "São Paulo",
                        "neighborhood": "Brás",
                        "zip_code": 12345,
                        "complement": "Apt 101",
                        "reference": "Near the store",
                    }
                ],
                "phone": "11999999999",
                "payment_formats": [
                    {"id": 1, "name": "Cash"},
                    {"id": 2, "name": "Credit Card"},
                    {"id": 3, "name": "Debit Card"},
                ],
            },
            "products": [
                {
                    "quantity": 2,
                    "product": {
                        "name": "Product X",
                        "description": "Description of product X",
                        "price": 19.99,
                        "images": [
                            "https://example.com/image1.jpg",
                            "https://example.com/image2.jpg",
                        ],
                        "categories": ["Category A", "Category B"],
                    },
                },
                {
                    "quantity": 1,
                    "product": {
                        "name": "Product Y",
                        "description": "Description of product Y",
                        "price": 9.99,
                        "images": [
                            "https://example.com/image3.jpg",
                            "https://example.com/image4.jpg",
                        ],
                        "categories": ["Category C", "Category D"],
                    },
                },
            ],
            "address": {
                "street": "Paulista Avenue",
                "number": 1000,
                "city": "São Paulo",
                "neighborhood": "Brás",
                "zip_code": 12345,
                "complement": "Apt 101",
                "reference": "Near the store",
            },
            "payment_format": {"id": 1, "name": "Cash"},
        }
    }

    await db_handler.disconnect_db()
