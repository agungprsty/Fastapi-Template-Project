# routes/user.py
from fastapi import APIRouter, Request, Depends, security
from dependency_injector.wiring import inject, Provide
from src.application.user.command.create_user import Create
from src.application.user.query.get_me import GetMe

from src.application.user.command import update_email
from src.application.user.command.delete import Delete
from src.application.user.command.update_localization import UpdateLocalization

from src.application.user.command.login_by_email import LoginByEmail
from src.domain.user.account.input_account import InputCreateAccount, InputLoginByEmail, InputUpdateEmailAccount, InputUpdateLocalozation
from src.domain.user.account.entities import AccountResposne, AccessTokenResponse
from src.domain.user.authentication.authentication import AccountAuthentication
from src.application.user.containers import UserContainer
from src.middleware.middleware import auth

user_routes = APIRouter(prefix="/account")

@user_routes.post(
    "/",
    tags=["Account"],
    summary="Create an Account",
    response_model=AccountResposne,
    response_model_exclude_unset=True
)
@inject
async def create(
    data: InputCreateAccount,
    command: Create = Depends(Provide[UserContainer.create_user_command]),
):
    return await command.handle(data)

@user_routes.post(
    "/login_by_email",
    tags=["Account"],
    summary="Login by Email",
    response_model=AccessTokenResponse,
    response_model_exclude_unset=True
)
@inject
async def login_by_email(
    data: InputLoginByEmail,
    command: LoginByEmail = Depends(Provide[UserContainer.command_login_by_email]),
):
    return await command.handle(data)

@user_routes.get(
    "/me",
    tags=["Account"],
    summary="Get my Account",
    response_model=AccountResposne,
    response_model_exclude_unset=True,
    dependencies=[
        Depends(Provide[
            security.HTTPBearer(), 
            auth
        ])
    ]
)
@inject
async def get_me(
    request: Request,
    query: GetMe = Depends(Provide[UserContainer.query_get_me]),
):
    return await query.handle(request.state.authentication)

@user_routes.put(
    "/",
    tags=["Account"],
    summary="Update Account",
    response_model=AccountResposne,
    response_model_exclude_unset=True,
    dependencies=[Depends(security.HTTPBearer())]
)
@inject
async def update(
    input_update: InputUpdateEmailAccount,
    authentication: AccountAuthentication = Depends(auth),
    command: update_email.UpdateEmail = Depends(Provide[UserContainer.command_update_email_account])
):
    return await command.handle(authentication, input_update)


@user_routes.put(
    "/update",
    tags=["Account"],
    summary="Update Account",
    response_model=AccountResposne,
    response_model_exclude_unset=True,
    dependencies=[Depends(security.HTTPBearer())]
)
@inject
async def update(
    input_update: InputUpdateEmailAccount,
    authentication: AccountAuthentication = Depends(auth),
    command: update_email.UpdateEmail = Depends(Provide[UserContainer.command_update_email_account])
):
    return await command.handle(authentication, input_update)

@user_routes.delete(
    "/",
    tags=["Account"],
    summary="Delete Account",
    response_model=None,
    response_model_exclude_unset=True,
    dependencies=[Depends(security.HTTPBearer())]
)
@inject
async def delete(
    authentication: AccountAuthentication = Depends(auth),
    command: Delete = Depends(Provide[UserContainer.command_delete])
):
    return await command.handle(authentication)

@user_routes.post(
    "/localization",
    tags=["Account"],
    summary="Update localization",
    response_model=AccountResposne,
    response_model_exclude_unset=True,
    dependencies=[Depends(security.HTTPBearer())]
)
@inject
async def update_localization(
    input_update: InputUpdateLocalozation,
    authentication: AccountResposne = Depends(auth),
    command: UpdateLocalization = Depends(Provide[UserContainer.command_update_localization])
):
    return await command.handle(authentication, input_update)