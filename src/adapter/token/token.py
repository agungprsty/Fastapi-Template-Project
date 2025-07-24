from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.domain.user.account.entities import Account
from config.config import Settings

class Token(object):
    def __init__(
            self,
            config: Settings

    ):
        self.__config = config

    def create_access_token(self, account: Account) -> jwt:
        try:
            token = jwt.encode({
                "exp": int((datetime.now() + (timedelta(hours=12))).timestamp()),
                "uid": account.id,
                "role": account.role.value,
            }, self.__config.jwt.secret_key, self.__config.jwt.algorithm)

            return token
        except JWTError:
            return None

    def validate_token(self, token_str: str):
        try:
            return jwt.decode(token_str, self.__config.jwt.secret_key, self.__config.jwt.algorithm)
        except JWTError:
            return None