import logging
from src.infrastructure.repositories.account_repository_impl import AccountRepositoryImpl
from src.domain.user.account.input_account import InputCreateAccount
from src.domain.user.account.entities import Account
from src.exception.http_error import BadRequestException

class Create(object):
    def __init__( self, account_repository: AccountRepositoryImpl) :
        self.__account_repository = account_repository
        self.__logging = logging.getLogger(__name__)
    
    async def handle(self, input_create_account: InputCreateAccount) -> Account:
        self.__logging.info('query get user success')
        user = await self.__account_repository.get_by_email(input_create_account.email)
        if user:
            raise BadRequestException(
                message="Email already registered",
                code="email_exists",
            )
        
        return await self.__account_repository.create(input_create_account)
