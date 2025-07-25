import logging
from src.infrastructure.repositories.account_repository_impl import AccountRepositoryImpl
from src.domain.user.account.input_account import InputLoginByEmail
from src.domain.user.account.entities import Account
from src.exception.http_error import BadRequestException
from src.adapter.token.token import Token
from src.domain.user.account.entities import AccessTokenResponse

class LoginByEmail(object):
    def __init__( self, account_repository: AccountRepositoryImpl, token: Token) :
        self.__account_repository = account_repository
        self.__token = token
        self.__logging = logging.getLogger(__name__)
    
    async def handle(self, input_login: InputLoginByEmail) -> Account:
        user = await self.__account_repository.get_by_email(input_login.email)

        if not user or not user.validate_password(input_login.password):
            raise BadRequestException(
                message="Invalid login",
                code="invalid_login"
            )
        
        token = self.__token.create_access_token(user)
        if not token:
            raise BadRequestException(
                message="Failed login"
            )
        
        return AccessTokenResponse(
            access_token=token
        )
