import bcrypt
from pydantic import field_validator, BaseModel, EmailStr
from src.exception import http_error

class InputCreateAccount(BaseModel):
    username: str
    email: str
    mobile_number: str
    password: str

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
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise http_error.BadRequestException(message="Password should more than 8 character")
        return value

class InputUpdateAccount(BaseModel):
    pass
    
class InputUpdateEmailAccount(InputUpdateAccount):
    email: EmailStr

    @field_validator('email')
    @classmethod
    def normalize_email(cls, v: EmailStr) -> EmailStr:
        return v.lower()

    def to_dict(self) -> dict:
        return {
            "email": self.email
        }