from beanie import Document
from pydantic import Field


class Address(Document):
    street: str = Field(..., title="Rua", max_length=100)
    number: int = Field(..., title="Número", ge=1)
    city: str = Field(..., title="Cidade", max_length=50)
    neighborhood: str = Field(..., title="Bairro", max_length=50)
    zip_code: int = Field(..., title="CEP", ge=10000, le=99999999)
    complement: str = Field(default="", title="Complemento", max_length=100)
    reference: str = Field(default="", title="Referência", max_length=100)

    class Settings:
        name = "addresses"
        alias_generator = str.lower
        schema_extra = {
            "example": {
                "street": "Avenida Paulista",
                "number": 1000,
                "city": "São Paulo",
                "neighborhood": "Brás",
                "zip_code": 12345,
                "complement": "Apto 101",
                "reference": "Perto da loja",
            }
        }
