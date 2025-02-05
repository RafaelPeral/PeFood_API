from beanie import Document
from pydantic import Field, EmailStr
from typing import List
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat


class User(Document):
    name: str = Field(..., title="Nome do usuário")
    email: EmailStr = Field(..., unique=True, title="E-mail do usuário")
    password: str = Field(..., title="Senha do usuário")
    addresses: List[Address] = Field(default_factory=list, title="Lista de endereços")
    tell: str = Field(..., title="Número de telefone")
    formas_de_pagamento: List[PaymentFormat] = Field(
        default_factory=list, title="Formas de pagamento"
    )

    class Settings:
        name = "users"
        alias_generator = str.lower
        schema_extra = {
            "example": {
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
            }
        }
