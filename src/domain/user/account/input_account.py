import bcrypt
from pydantic import field_validator, BaseModel

class InputCreateAccount(BaseModel):
    username: str
    email: str
    mobile_number: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Invalid password")
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