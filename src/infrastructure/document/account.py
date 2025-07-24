import pymongo
from typing import Optional
from pydantic import Field
from datetime import datetime
from beanie import Document, Indexed, before_event, Save
from src.domain.user.account.entities import Localization
from src.domain.user.account.enum import AccountStatus, AuthenticationRole

class Account(Document):
    username: str = Field(...)
    email: str = Field(..., index=True, unique=True)
    mobile_number: str
    password_hash: str

    status: AccountStatus = Field(default=AccountStatus.ACTIVE)
    role: AuthenticationRole = Field(default=AuthenticationRole.USER)

    localization: Optional[Localization] = Field(default=Localization())

    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    updated_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    deleted_at: int = Field(default=0)

    @before_event(Save)
    async def update_timestamp(self):
        self.updated_at = int(datetime.now().timestamp() * 1000)

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
    
    