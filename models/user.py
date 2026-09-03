from pydantic import BaseModel, Field, field_validator
from typing import Optional

# PASSWORD_PATTERN = (
#     r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[~!@#$%^&*()_\-+={}|:;'?/><]).+$"
# )


class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    email: str = Field(pattern=r"^[\w\.-]{2,15}@gmail\.com$")
    age: int = Field(ge=1, le=120)
    phone_number: str = Field(pattern=r"^\+91[0-9]{10}$")
    gender: str = Field(pattern=r"^[Mm]ale$|^[Ff]emale$")
    password: str = Field(min_length=8, max_length=12)
    confirm_password: str
    home_address: Optional[str] = Field(default=None, max_length=100)
    office_address: Optional[str] = Field(default=None, max_length=100)
    occupation: Optional[str] = Field(default=None, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        if not any(c in "~!@#$%^&*()_-+={}|:;'?/><" for c in value):
            raise ValueError("Password must have at least one special character")
        return value

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, info):
        if "password" in info.data and confirm_password != info.data["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    phone_number: str
    gender: str
    home_address: Optional[str] = None
    office_address: Optional[str] = None
    occupation: Optional[str] = None


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    home_address: Optional[str] = None
    office_address: Optional[str] = None
    occupation: Optional[str] = None
