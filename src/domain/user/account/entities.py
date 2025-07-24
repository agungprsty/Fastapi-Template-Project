import bcrypt
from .enum import AccountStatus, AuthenticationRole as Role
from pydantic import BaseModel

class Account(BaseModel):
    id: str
    username: str
    email: str
    mobile_number: str
    password_hash: str
    status: AccountStatus
    role: Role
    created_at: int
    updated_at: int
    deleted_at: int

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email
        }

    def validate_password(self, passwd_str: str) -> bool:
        return bcrypt.checkpw(
            passwd_str.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

class AccountResposne(BaseModel):
    id: str
    username: str
    email: str
    mobile_number: str
    status: AccountStatus
    role: Role
    created_at: int
    updated_at: int
    deleted_at: int

class AccessTokenResponse(BaseModel):
    access_token: str