import bcrypt
import datetime
from typing import Optional
from .enum import Lang, DateFormat, TimeFormat, Currency, NumberFormat

from pydantic import (
    field_validator, 
    Field, 
    BaseModel, 
    EmailStr
)
from src.exception import http_error

class InputCreateAccount(BaseModel):
    username: str = Field(..., example="markonah")
    email: str = Field(..., example="markonah@gmail.com")
    mobile_number: str = Field(..., example="696969696969")
    password: str = Field(..., example="markonah69")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise http_error.BadRequestException(message="Invalid password")
        return value

    def __hashed_password(self):
        return bcrypt.hashpw(
        self.password.encode('utf-8'), 
        bcrypt.gensalt()
        
    ).decode('utf-8')
    
    def to_input_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "mobile_number": self.mobile_number,
            "password_hash": self.__hashed_password()
        }

class InputLoginByEmail(BaseModel):
    email: str = Field(..., example="markonah@gmail.com")
    password: str = Field(..., example="markonah69")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise http_error.BadRequestException(message="Password should more than 8 character")
        return value

class InputUpdateAccount(BaseModel):
    pass
    
class InputUpdateEmailAccount(InputUpdateAccount):
    username: Optional[str] = Field(None, example="markonah")
    email: Optional[EmailStr] = Field(None, example="markonah@gmail.com")

    @field_validator('email')
    @classmethod
    def normalize_email(cls, v: EmailStr) -> EmailStr:
        return v.lower()

    def to_dict(self) -> dict:
        return {
            "email": self.email
        }

class InputUpdateLocalozation(InputUpdateAccount):
    lang: Optional[str] = Field(None, example=Lang.ID)
    date_format: Optional[str] = Field(None, example=DateFormat.DDMMYY)
    time_format: Optional[str] = Field(None, example=TimeFormat._24H)
    number_format: Optional[str] = Field(None, example=NumberFormat.TITIK)
    currency: Optional[str] = Field(None, example=Currency.IDR)