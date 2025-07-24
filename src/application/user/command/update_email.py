import logging
from src.infrastructure.repositories.account_repository_impl import AccountRepositoryImpl
from src.domain.user.account.input_account import InputUpdateEmailAccount
from src.domain.user.account.entities import Account
from src.exception.http_error import BadRequestException
from src.domain.user.authentication.authentication import AccountAuthentication

class UpdateEmail(object):
    def __init__( self, account_repository: AccountRepositoryImpl) :
        self.__account_repository = account_repository
        self.__logging = logging.getLogger(__name__)
    
    async def handle(self, authentication: AccountAuthentication, input_update_account: InputUpdateEmailAccount) -> Account:
        user = await self.__account_repository.update(str(authentication.id), input_update_account)
        if not user:
            raise BadRequestException(
                message="Failed to update",
                code="update_failed",
            )
        
        return user