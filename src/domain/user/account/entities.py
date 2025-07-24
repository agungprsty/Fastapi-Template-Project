import bcrypt
from .enum import AccountStatus, AuthenticationRole as Role, DateFormat, TimeFormat, NumberFormat, Currency, Lang
from pydantic import BaseModel, Field

class Localization(BaseModel):
    lang: Lang = Field(default=Lang.ID, example=Lang.ID)
    date_format: DateFormat = Field(default=DateFormat.DDMMYY, example=DateFormat.DDMMYY)
    time_format: TimeFormat = Field(default=TimeFormat._24H, example=TimeFormat._24H)
    number_format: NumberFormat = Field(default=NumberFormat.TITIK, example=NumberFormat.TITIK)
    currency: Currency = Field(default=Currency.IDR, example=Currency.IDR)

class Account(BaseModel):
    id: str
    username: str
    email: str
    mobile_number: str
    password_hash: str
    status: AccountStatus
    role: Role
    localization: Localization
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
    localization: Localization
    created_at: int
    updated_at: int
    deleted_at: int

class AccessTokenResponse(BaseModel):
    access_token: str