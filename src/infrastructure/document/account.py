import pymongo
from pydantic import Field
from datetime import datetime
from beanie import Document, Indexed
from src.domain.user.account.enum import AccountStatus, AuthenticationRole

class Account(Document):
    username: str = Field(...)
    email: str = Field(..., index=True, unique=True)
    mobile_number: str
    password_hash: str

    status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    role: AuthenticationRole = Field(default=AuthenticationRole.USER)

    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    deleted_at: int = Field(default=0)

    class Settings:
        name = "account"
        indexes = [
            [
                ("username", pymongo.TEXT),
                ("email", pymongo.TEXT),
                ("mobile_number", pymongo.TEXT),
                ("status", pymongo.TEXT),
            ],
        ]
