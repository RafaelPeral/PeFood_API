from beanie import Document
from pydantic import Field, EmailStr, field_validator
from typing import List
import bcrypt
import re
from src.model.entities.address import Address
from src.model.entities.payment_format import PaymentFormat


class User(Document):
    name: str = Field(..., title="User Name")
    email: EmailStr = Field(..., json_schema_extra={"unique": True}, title="User Email")
    password: str = Field(..., title="Password")
    addresses: List[Address] = Field(default_factory=list, title="Address List")
    phone: str = Field(..., title="Phone Number")
    payment_formats: List[PaymentFormat] = Field(
        default_factory=list, title="Payment Methods"
    )

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", name):
            raise ValueError("Name cannot contain numbers or special characters")
        return name.strip()

    @field_validator("phone")
    def validate_phone(cls, phone: str) -> str:
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")
        if not (10 <= len(phone) <= 15):
            raise ValueError("Phone number must be between 10 and 15 digits long")
        return phone

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    class Settings:
        name = "users"
        alias_generator = str.lower
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "password": "SecureP@ss123",
                "addresses": [
                    {
                        "street": "Fifth Avenue",
                        "number": 1000,
                        "city": "New York",
                        "neighborhood": "Manhattan",
                        "zip_code": 10001,
                        "complement": "Apt 101",
                        "reference": "Near the shopping mall",
                    }
                ],
                "phone": "1234567890",
                "payment_formats": [
                    {"id": "65d1b5e5f3a3b8b7e2f8c4a1", "name": "Cash"},
                    {"id": "65d1b5e5f3a3b8b7e2f8c4a2", "name": "Credit Card"},
                    {"id": "65d1b5e5f3a3b8b7e2f8c4a3", "name": "Debit Card"},
                ],
            }
        }
