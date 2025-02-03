from beanie import Document


class PaymentFormat(Document):
    id: int
    name: str

    class Config:
        schema_extra = {"example": {"id": 1, "name": "Dinheiro"}}
