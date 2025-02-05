from beanie import Document
from pydantic import Field


class PaymentFormat(Document):
    name: str = Field(..., title="Nome da Forma de Pagamento", max_length=50)

    class Settings:
        name = "payment_formats"
        alias_generator = str.lower
        schema_extra = {
            "example": {
                "name": "Dinheiro",
            }
        }
