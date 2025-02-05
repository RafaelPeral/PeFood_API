from beanie import Document
from pydantic import Field, field_validator
from typing import ClassVar


class Address(Document):
    street: str = Field(..., title="Street", max_length=100)
    number: int = Field(..., title="Number", ge=1)
    city: str = Field(..., title="City", max_length=50)
    neighborhood: str = Field(..., title="Neighborhood", max_length=50)
    zip_code: int = Field(..., title="ZIP Code", ge=10000, le=99999999)
    complement: str = Field(default="", title="Complement", max_length=100)
    reference: str = Field(default="", title="Reference", max_length=100)

    @field_validator("zip_code")
    def validate_zip_code(cls, zip_code: int) -> int:
        zip_str = str(zip_code)
        if len(zip_str) not in [8, 5]:
            raise ValueError("ZIP Code must have 5 or 8 digits")
        return zip_code

    @field_validator("city", "neighborhood", "street")
    def validate_text_fields(cls, value: str) -> str:
        if not value.replace(" ", "").isalpha():
            raise ValueError("The field must contain only letters")
        return value

    class Settings:
        name = "addresses"
        alias_generator: ClassVar = str.lower
        schema_extra = {
            "example": {
                "street": "Avenida Paulista",
                "number": 1000,
                "city": "São Paulo",
                "neighborhood": "Brás",
                "zip_code": 12345,
                "complement": "Apt 101",
                "reference": "Near the store",
            }
        }
