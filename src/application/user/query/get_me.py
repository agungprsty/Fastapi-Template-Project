import logging
from src.infrastructure.repositories.account_repository_impl import AccountRepositoryImpl
from src.domain.user.account.input_account import InputCreateAccount
from src.domain.user.account.entities import Account
from src.exception.http_error import NotFoundException
from src.domain.user.authentication.authentication import AccountAuthentication

class GetMe(object):
    def __init__( self, account_repository: AccountRepositoryImpl) :
        self.__account_repository = account_repository
        self.__logging = logging.getLogger(__name__)
    
    async def handle(self, authentication: AccountAuthentication) -> Account:
        user = await self.__account_repository.get_by_id(authentication.id)
        if not user:
            raise NotFoundException()

        return user
