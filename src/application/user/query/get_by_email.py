from src.infrastructure.repositories.account_repository_impl import AccountRepositoryImpl
from src.domain.user.account.entities import Account
from src.exception.http_error import NotFoundException

class GetByEmail(object):
    def __init__( self, account_repository: AccountRepositoryImpl) :
        self.__account_repository = account_repository
    
    async def handle(self, email: str) -> Account:
        user = await self.__account_repository.get_by_email(email)
        if not user:
            raise NotFoundException()

        return user
