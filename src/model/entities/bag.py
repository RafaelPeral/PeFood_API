from beanie import Document
from typing import List
from pydantic import Field
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat
from src.model.entities.user import User
from src.model.entities.product import Product


class ProductItem(Document):
    quantity: int = Field(..., title="Quantidade", ge=1)
    product: Product = Field(..., title="Produto")


class Bag(Document):
    user: User = Field(..., title="Usuário")
    products: List[ProductItem] = Field(..., title="Lista de Produtos")
    address: Address = Field(..., title="Endereço de Entrega")
    payment_format: PaymentFormat = Field(..., title="Forma de Pagamento")

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
                            "street": "Avenida Paulista",
                            "number": 1000,
                            "city": "São Paulo",
                            "neighborhood": "Brás",
                            "zip_code": 12345,
                            "complement": "Apto 101",
                            "reference": "Perto da loja",
                        }
                    ],
                    "tell": "11999999999",
                    "formas_de_pagamento": [
                        {"id": 1, "name": "Dinheiro"},
                        {"id": 2, "name": "Cartão de crédito"},
                        {"id": 3, "name": "Cartão de débito"},
                    ],
                },
                "products": [
                    {
                        "quantity": 2,
                        "product": {
                            "name": "Produto X",
                            "description": "Descrição do produto X",
                            "price": 19.99,
                            "images": [
                                "https://example.com/image1.jpg",
                                "https://example.com/image2.jpg",
                            ],
                            "categories": ["Categoria A", "Categoria B"],
                        },
                    },
                    {
                        "quantity": 1,
                        "product": {
                            "name": "Produto Y",
                            "description": "Descrição do produto Y",
                            "price": 9.99,
                            "images": [
                                "https://example.com/image3.jpg",
                                "https://example.com/image4.jpg",
                            ],
                            "categories": ["Categoria C", "Categoria D"],
                        },
                    },
                ],
                "address": {
                    "street": "Avenida Paulista",
                    "number": 1000,
                    "city": "São Paulo",
                    "neighborhood": "Brás",
                    "zip_code": 12345,
                    "complement": "Apto 101",
                    "reference": "Perto da loja",
                },
                "payment_format": {"id": 1, "name": "Dinheiro"},
            }
        }
