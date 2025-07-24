from fastapi import Request
from jose import jwt, JWTError, ExpiredSignatureError
from src.exception.http_error import BadRequestException
from config.config import Settings
from src.domain.user.authentication.authentication import AccountAuthentication, AuthenticationRole
from src.application.user.containers import UserContainer
from src.domain.user.account.entities import Account

async def jwt_auth(
    request: Request, 
):
    config: Settings = request.app.container.config()
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise BadRequestException(
            message="Invalid Authorization header"
        )

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, config.jwt.secret_key, algorithms=config.jwt.algorithm)
        user: Account = await UserContainer.query_get_by_id().handle(payload)
        if not user:
            raise BadRequestException("Invalid token")

        request.state.authentication = AccountAuthentication(
            id=user.id,
            role=AuthenticationRole[user.role.name]
        )

    except ExpiredSignatureError:
        raise BadRequestException(
            message="Token expired"
        )
    except JWTError:
        raise BadRequestException(
            message="Invalid token"
        )