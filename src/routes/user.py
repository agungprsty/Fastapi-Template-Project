# routes/user.py
from fastapi import APIRouter, Request, Depends, security
from dependency_injector.wiring import inject, Provide
from src.application.user.command.create_user import Create
from src.application.user.query.get_me import GetMe

from src.application.user.command import update_email

from src.application.user.command.login_by_email import LoginByEmail
from src.domain.user.account.input_account import InputCreateAccount, InputLoginByEmail, InputUpdateEmailAccount
from src.domain.user.account.entities import AccountResposne, AccessTokenResponse
from src.application.user.containers import UserContainer
from src.utils.middleware import jwt_auth

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
        Depends(security.HTTPBearer()), 
        Depends(jwt_auth)
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
    dependencies=[
        Depends(security.HTTPBearer()), 
        Depends(jwt_auth)
    ]
)
@inject
async def update(
    request: Request,
    input_update: InputUpdateEmailAccount,
    command: update_email.UpdateEmail = Depends(Provide[UserContainer.command_update_email_account])
):
    return await command.handle(request.state.authentication, input_update)