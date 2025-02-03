from beanie import Document
from typing import List
from model.entities.address import Address
from model.entities.payment_format import PaymentFormat


class User(Document):
    id: int
    name: str
    email: str
    password: str
    addresses: List[Address]
    tell: str
    formas_de_pagamento: List[PaymentFormat]

    class Config:
        schema_extra = {
            "example": {
                "name": "Rafael Peral",
                "email": "7tqZS@example.com",
                "password": "123456",
                "addresses": [
                    {
                        "street": "Avenida Paulista",
                        "number": 1000,
                        "city": "São Paulo",
                        "neighborhood": "Brás",
                        "zip_code": 12345,
                        "complement": "Apto 101",
                        "reference": "Perto da loja",
                    }
                ],
                "tell": "11999999999",
                "formas_de_pagamento": [
                    {"id": 1, "name": "Dinheiro"},
                    {"id": 2, "name": "Cartão de crédito"},
                    {"id": 3, "name": "Cartão de débito"},
                ],
            }
        }
