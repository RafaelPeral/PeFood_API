from beanie import Document


class Address(Document):
    street: str
    number: int
    city: str
    neighborhood: str
    zip_code: int
    complement: str
    reference: str

    class Config:
        schema_extra = {
            "example": {
                "street": "Avenida Paulista",
                "number": 1000,
                "city": "São Paulo",
                "neighborhood": "Brás",
                "zip_code": 12345,
                "complement": "Apto 101",
                "reference": "Perto da loja",
            }
        }
