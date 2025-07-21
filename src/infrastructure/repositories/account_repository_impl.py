from abc import abstractmethod
from typing import Protocol, Optional, List
from src.domain.user.account.entities import Account
from src.domain.user.account.input_account import InputCreateAccount

class AccountRepositoryImpl(Protocol):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Account]:
        ...

    @abstractmethod
    async def create(self, input_create_account: InputCreateAccount) -> Account:
        ...

    @abstractmethod
    async def list(self) -> List[Account]:
        ...
