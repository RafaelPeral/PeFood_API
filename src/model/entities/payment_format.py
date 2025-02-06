import re
from beanie import Document
from pydantic import Field, field_validator


class PaymentFormat(Document):
    name: str = Field(..., title="Payment Method Name", max_length=50)

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        name = name.strip()
        if len(name) < 3:
            raise ValueError(
                "The payment method name must be at least 3 characters long"
            )
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", name):
            raise ValueError(
                "The payment method name cannot contain numbers or special characters"
            )
        return name

    class Settings:
        name = "payment_formats"
        alias_generator = str.lower
        schema_extra = {
            "example": {
                "name": "Cash",
            }
        }
