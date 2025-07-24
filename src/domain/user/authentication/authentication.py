from .enum import AuthenticationRole
from pydantic import BaseModel

class Authentication(BaseModel):
    ...


class AccountAuthentication(Authentication):
    id: str
    role: AuthenticationRole