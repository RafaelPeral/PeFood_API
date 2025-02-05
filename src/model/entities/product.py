from typing import List
from beanie import Document
from pydantic import Field


class Product(Document):
    name: str = Field(..., title="Nome do Produto", max_length=100)
    description: str = Field(..., title="Descrição", max_length=500)
    price: float = Field(..., gt=0, title="Preço")
    images: List[str] = Field(default_factory=list, title="Imagens do Produto")
    categories: List[str] = Field(default_factory=list, title="Categorias")

    class Settings:
        name = "products"
        alias_generator = str.lower
        schema_extra = {
            "example": {
                "name": "Produto X",
                "description": "Descrição do produto X",
                "price": 19.99,
                "images": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg",
                ],
                "categories": ["Categoria A", "Categoria B"],
            }
        }
