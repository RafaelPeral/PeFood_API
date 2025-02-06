import re
from typing import List
from beanie import Document
from pydantic import Field, field_validator


class Product(Document):
    name: str = Field(..., title="Product Name", max_length=100)
    description: str = Field(..., title="Description", max_length=500)
    price: float = Field(..., title="Price")
    images: List[str] = Field(default_factory=list, title="Product Images")
    categories: List[str] = Field(default_factory=list, title="Categories")

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name) < 3:
            raise ValueError("The product name must be at least 3 characters long")
        if not re.match(r"^[a-zA-ZÀ-ÿ0-9\s]+$", name):
            raise ValueError("The product name cannot contain special characters")
        return name.strip()

    @field_validator("description")
    def validate_description(cls, description: str) -> str:
        if len(description) < 10:
            raise ValueError("The description must be at least 10 characters long")
        return description.strip()

    @field_validator("price")
    def validate_price(cls, price: float) -> float:
        if price < 0:
            raise ValueError("The price must be greater than zero")
        return round(price, 2)

    @field_validator("images")
    def validate_images(cls, images: List[str]) -> List[str]:
        if len(images) > 5:
            raise ValueError("A product can have a maximum of 5 images")
        for image in images:
            if not re.match(r"^(http|https)://", image):
                raise ValueError(f"Invalid image URL: {image}")
        return images

    @field_validator("categories")
    def validate_categories(cls, categories: List[str]) -> List[str]:
        if not categories:
            raise ValueError("The product must have at least one category")
        for category in categories:
            if len(category) < 3:
                raise ValueError(
                    f"The category '{category}' must be at least 3 characters long"
                )
        return categories

    class Settings:
        name = "products"
        alias_generator = str.lower
        schema_extra = {
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
