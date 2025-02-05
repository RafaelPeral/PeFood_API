from beanie import Document
from typing import List
from pydantic import Field, field_validator
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat
from src.model.entities.user import User
from src.model.entities.product import Product


class ProductItem(Document):
    quantity: int = Field(..., title="Quantity", ge=1)
    product: Product = Field(..., title="Product")

    @field_validator("quantity")
    def validate_quantity(cls, quantity: int) -> int:
        if quantity > 1000:
            raise ValueError(
                "The quantity of a single product cannot exceed 1000 units"
            )
        return quantity


class Bag(Document):
    user: User = Field(..., title="User")
    products: List[ProductItem] = Field(..., title="Product List")
    address: Address = Field(..., title="Delivery Address")
    payment_format: PaymentFormat = Field(..., title="Payment Method")

    @field_validator("products")
    def validate_products(cls, products: List[ProductItem]) -> List[ProductItem]:
        if not products:
            raise ValueError("The product list cannot be empty")
        return products

    class Settings:
        name = "bags"
        alias_generator = str.lower
        schema_extra = {
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
