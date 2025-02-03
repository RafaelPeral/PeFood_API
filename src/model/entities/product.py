from beanie import Document
from typing import List


class Product(Document):
    id: int
    name: str
    description: str
    price: float
    images: List[str]
    categories: List[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Produto X",
                "description": "Descrição do produto X",
                "price": 19.99,
                "images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg",
                ],
                "categories": ["Categoria A", "Categoria B"],
            }
        }
